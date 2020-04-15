#include <iostream>
#include <string>
#include <regex>
#include "wrapper.hpp"
#include "killers.hpp"

struct message
{
	uint32_t process_id;
	char data[4096 - sizeof(uint32_t)];
};

void* open_event(int access, std::wstring event)
{
	auto handle = wrapper::open_event(
		access,
		false,
		event);
	if (!handle)
	{
		handle = wrapper::create_event(
			nullptr,
			false,
			true, // maybe false DBWIN_DATA_READY
			event);
	}

	return handle;
}

void* open_mapping(std::wstring mapping)
{
	auto handle = wrapper::open_file_mapping(
		FILE_MAP_READ,
		false,
		mapping);
	if (!handle)
	{
		handle = wrapper::create_file_mapping(
			INVALID_HANDLE_VALUE,
			nullptr,
			PAGE_READWRITE,
			0,
			sizeof(message), // maybe struct message
			mapping);
	}

	return handle;
}

int find_process(std::string process_name)
{
	PROCESSENTRY32 entry;
	entry.dwSize = sizeof(PROCESSENTRY32);
	auto snapshot = wrapper::create_toolhelp32_snapshot(TH32CS_SNAPPROCESS, 0);
	int process_id = -1;

	if (wrapper::process32_first(snapshot, &entry))
	{
		while (wrapper::process32_next(snapshot, &entry))
		{
			auto wname = std::wstring(entry.szExeFile);
			auto name = std::string(wname.begin(), wname.end());
			if (name.find(process_name) != std::string::npos)
			{
				process_id = entry.th32ProcessID;
				break;
			}
		}
	}

	wrapper::close_handle(snapshot);

	return process_id;
}

int main(int argc, char** argv)
{
	const auto process_id = find_process("DeadByDaylight-Win64-Shipping.exe");

	const std::regex character_id_pattern("Spawn new pawn characterId (\\d+)\\.");
	const std::regex steam_id_pattern("Session:GameSession PlayerId:([0-9\\-a-z]+)\\|(\\d+)");
	const std::regex killer_pattern("MatchMembersA=\\[\\\"([a-z0-9\\-]+)\\\"\\]");
	auto buffer_ready = open_event(
		EVENT_ALL_ACCESS,
		L"DBWIN_BUFFER_READY");
	auto data_ready = open_event(
		SYNCHRONIZE,
		L"DBWIN_DATA_READY");
	auto file = open_mapping(
		L"DBWIN_BUFFER");
	auto buffer = reinterpret_cast<message*>(
		wrapper::map_view_of_file(
			file,
			SECTION_MAP_READ,
			0, 0, 0));

	std::string killer_id;

	while (wrapper::wait_for_single_object(
		data_ready,
		INFINITE) == WAIT_OBJECT_0)
	{
		if (buffer->process_id == process_id)
		{
			auto message = std::string(buffer->data);
			std::smatch matches;

			if (std::regex_search(message, matches, character_id_pattern))
			{
				auto character_id = std::stoi(matches[1].str());
				auto killer = KILLERS.find(character_id);
				if (killer != KILLERS.end())
				{
					std::cout << "Killer: " << killer->second << std::endl;
				}
			}
			else if (std::regex_search(message, matches, steam_id_pattern))
			{
				auto player_id = matches[1].str();
				auto steam_id = matches[2].str();
				if (player_id == killer_id)
				{
					std::cout << "Killer Steam Profile: https://steamcommunity.com/profiles/" << steam_id << std::endl;
				}
			}
			else if (std::regex_search(message, matches, killer_pattern))
			{
				killer_id = matches[1].str();
				std::cout << "Found Killer PlayerID: " << killer_id << std::endl;
			}
		}

		wrapper::set_event(buffer_ready);
	}

	wrapper::unmap_view_of_file(buffer);
	wrapper::close_handle(file);
	wrapper::close_handle(buffer_ready);
	wrapper::close_handle(data_ready);

	return 0;
}