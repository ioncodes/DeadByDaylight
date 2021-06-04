# DeadByDaylight
Research material and PoC for bugs found during the reversal of the game Dead by Daylight. All information provided is for educational purpose and shows possible pitfalls game developers may fall into. For an in depth analysis please refer to the [official article](https://layle.me/dead-by-daylight/). You can reach out to me on [Twitter](https://twitter.com/layle_ctf) for any questions.  
**Do not use this to get an advantage in the game or in any other game**.

## dbd_killer_finder
The project can be built using Visual Studio. The tool allows you to read Windows' message buffer just like DebugView does, allowing you to parse debug messages of other processes in realtime. The tool includes basic regular expressions filtering out the killer and the steam profile.

## dbd_injector
This project is basic Python3 code. An installation of `mitmdump` is expected. The scripts allow you to perform various actions such as ranking up your profile and decrypting inventories. Issue the following command to get started:  

```
mitmdump -s authenticator.py -q
```
