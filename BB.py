from py2neo import Graph
import sys, getopt

def bOM(g):
  print('\n(s) standings')
  print('(t) team results')
  print('(q) quit\n')

  standings = input('What do you want to see: ')
  if standings == 'q':
    exit()
  # if standings is not 's' and standings is not 't':
  #   print ('Invalid input!')
  if standings == 's':
    print ('\nTEAM                   WINS LOSSES   TIES PERCENT')
    print ('-------------------- ------ ------ ------ -------')
    def accountCost(g, code):
      query = """
        match (v:Team{code: {code}})-[r:plays_games]->(h:Team)
        return v.name as vname, v.code as vcode, h.code as hcode, r.date as date, r.vscore as vscore, r.hscore as hscore
      """
      res = g.run(query, code=code)
      v_wincount = v_losecount = v_tiecount = 0
      for r in res:
        if int(r['vscore']) > int(r['hscore']):
          v_wincount += 1
        elif int(r['vscore']) < int(r['hscore']):
          v_losecount += 1
        else:
          v_tiecount +=1
      team_name = r['vname']

      h_wincount = h_losecount = h_tiecount = 0
      query = """
        match (v:Team)-[r:plays_games]->(h:Team{code: {code}})
        return v.code as vcode, h.code as hcode, r.date as date, r.vscore as vscore, r.hscore as hscore
      """
      res = g.run(query, code=code)
      for r in res:
        if int(r['vscore']) < int(r['hscore']):
          h_wincount += 1
        elif int(r['vscore']) > int(r['hscore']):
          h_losecount += 1
        else:
          h_tiecount +=1
      win = v_wincount+h_wincount
      lose = v_losecount+h_losecount
      tie = v_tiecount+h_tiecount
      print (team_name, '        ', win, '      ', lose, '    ', tie, '    ', (win+0.5*tie)/(win+lose+tie))
    spe_code = ['ARI', 'ATL', 'CHC', 'CLE', 'STL']
    standings_rst = []
    for item in spe_code:
      standings_rst.append(accountCost(g, item))   
    print (standings_rst)
    bOM(g)

  code = input('Enter team code (e.g. ARI, ATL, CHC, CLE, STL):')
  if code not in ['ARI', 'ATL', 'CHC', 'CLE', 'STL']:
    print ('\nInvalid Code\n')
    bOM(g)

  if standings == 't':
    def teamResults(g, code):
      game_rst = []
      query = """
        match (v:Team{code: {code}})-[r:plays_games]->(h:Team)
        return v.name as vname, v.location as vlocation, v.code as vcode, h.code as hcode, h.name as hname, r.date as date, r.vscore as vscore, r.hscore as hscore
      """
      res = g.run(query, code=code)
      
      for r in res:
        if r['vscore'] > r['hscore']:
          result = 'WIN'
        elif r['vscore'] < r['hscore']:
          result = 'LOSE'
        else:
          result = 'TIE'
        game_rst.append([r['date'], '     ', 'at', r['hname'], r['vscore'], r['hscore'], result])
      location = r['vlocation']
      name = r['vname']
      print ('\n', location, name, '\n')
      print ('DATE             OPPONENT    US  THEM RESULT')

      ### Input team as host team ###
      query = """
        match (v:Team)-[r:plays_games]->(h:Team{code: {code}})
        return v.name as vname, v.code as vcode, h.code as hcode, r.date as date, r.vscore as vscore, r.hscore as hscore
      """
      res = g.run(query, code=code)
      for r in res:
        if r['vscore'] < r['hscore']:
          result = 'WIN'
        elif r['vscore'] > r['hscore']:
          result = 'LOSE'
        else:
          result = 'TIE'
        game_rst.append([r['date'], '     ', r['vname'], '  ', r['hscore'], '  ', r['vscore'], '  ', result])
      for item in sorted(game_rst):
        for i in item:
          print (i, end =" ")
        print (' ')

    print (teamResults(g, code))
  elif standings is not 's' and standings is not 't':
    print ('\nInvalid Code!')

  bOM(g)

def main():
  g = Graph(auth=('neo4j','emma15emma'))
  rst = bOM(g)
  return (rst)

main()
