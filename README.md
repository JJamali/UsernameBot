# UsernameBot

A bot I made to remove those pesky low value ASCII characters in front of my peers' names on discord.


UsernameBot automatically detects and updates usernames when they are changed, but will not run on the initial usernames upon joining. 
Use `!banish` once UsernameBot joins to manually banish unsightly usernames to the bottom of the user list.
For persistent users that try to use the workaround of placing numbers, or the letter 'A' at the start of their names, 
there is the `!smite [@user mention here]` command to blacklist them onto an SQLite3 database. Once a user is smited,
they will be sent to the bottom of the user list regardless of any username changes. This command is only usable by 
server administrators. 
