from Website_to_CSV_Functions import *
from Player_Class import *

from concurrent.futures import ThreadPoolExecutor


def Get_Players_and_Ids_From_CSV_File(filename):
    Players_temp={}
    with open(filename,'r') as fout:
        reader = csv.reader(fout)
        for row in reader:
            if row[0] != 'Player Id':
                player = Player()
                player.Assign_Variables_From_CSV(row)
                Players_temp[player.player_id]=player
    return Players_temp

# Only one should be executed based on if you want to get the player names and
# ids from a csv file or from the website.
print("Getting player IDs")
# Players = get_and_store_all_players_names_and_ids('Player_Ids_Urls.csv')
Players = Get_Players_and_Ids_From_CSV_File('Player_Ids_Urls.csv')

# Get Basic Statistics
print("Getting basic player statistics")

with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
    ps = []
    for player_id in Players:
        ps.append(Player_Basic_Stats(Players[player_id]))

    count = 0

    def callback():
        global count

        if count % 100 == 0 and count != 0:
            print("Processed {} of {} players".format(count, len(ps)))

        count += 1

    pool.map(lambda p: p.Get_and_Store_Basic_Stats('Basic_Stats.csv', callback), ps)

# Get Career Stats
print("Done getting basic player statistics")
print("Getting career player statistics")

count = 1
for player_id in Players:
    player = Career_Stats(Players[player_id])
    if Check_for_Stats_Webpage(player,'Career Stats'):
        player.Get_and_Store_Career_Stats()
    if count % 100 == 0:
        print('Processed career stats for %d out of %d players' % (count, len(Players)))
    count+=1

# Get Game Logs
print("Done getting player career statistics")
print("Getting player game logs")

count = 1
for player_id in Players:
    player = Game_Logs(Players[player_id])
    if Check_for_Stats_Webpage(player,'Game Logs'):
        player.Get_and_Store_Game_Logs()
    if count % 100 == 0:
        print('Processed game logs for %d out of %d players' % (count, len(Players)))
    count+=1


