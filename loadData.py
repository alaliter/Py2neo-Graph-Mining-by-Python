import sys
import csv
from py2neo import Graph, Node, Relationship, NodeMatcher

def loadTeams(g,fname):
  with open(fname, 'r') as f:
    rows = list(csv.reader(f))

  nodes = []
  for row in rows:
    r = row[0].split(':')
    #n = Node("Team", name=r[0], location=r[1], code=r[2])
    #query = f'({{r[2]}:Team {{name: "{r[0]}", location: "{r[1]}", code: "{r[2]}"}}})'
    query = f'({r[2]}:Team {{name:"{r[0]}", location:"{r[1]}", code: "{r[2]}"}})'
    nodes.append(query)
  return nodes
    
def loadGames(g,fname):
  with open(fname, 'r') as f:
    rows = list(csv.reader(f))
  #matcher = NodeMatcher(g)
  rels = []
  for row in rows:
    r = row[0].split(':')
    #v = matcher.match("Team", code=r[1]).first()
    #h = matcher.match("Team", code=r[2]).first()
    #rel = Relationship(v, "plays_games", h, date=r[0], vscore=int(r[3]), hscore=int(r[4]))
    #query = f'({r[1]})-[:plays_games {{date: "{r[0]}", vscore: "{r[3]}", hscore: "{r[4]}"}}]->({r[2]})'
    
    query = f'({r[1]})-[:plays_games {{date:"{r[0]}", vscore:"{r[3]}", hscore:"{r[4]}"}}]->({r[2]})'
    rels.append(query)
    # query = f'''
    #   CREATE
    #   ({r["code"]}:Team {{name: "{r["name"]}"}}),
    #   ...,
    #   (r["code"])-[:plays_games {{date: "{r[0]}", vscore: "{r[3]}" }}]->(STL)
    # '''
    # g.run(query)
    #print (rel)
    #g.create(rel)
  return rels

def dupliGames(g,fname1, fname2):
  ## load shows using cypher statement; other method does not add 
  ## multiple relationships with same name between two nodes
  ## Bug in py2neo
  # with open(fname, 'r') as f:
  #   rows = list(csv.reader(f))
  # matcher = NodeMatcher(g)
  # for row in rows:
  #   r = row[0].split(':')
  all_node = loadTeams(g,fname1)
  all_relat = loadGames(g, fname2)
  #matcher = NodeMatcher(g)
  everything = all_node + all_relat
  # for one_node in all_node, one_relat in all_relat:
  # ({team:Team {{name: '{one_node["name"]}', location: '{one_node["location"]}', code: '{one_node["code"]}'}}),
  query = f'CREATE '
  for e in everything:
    query+= e + ','
  query = query[:-1] + ';'
  g.run(query)


def main():
  g = Graph(auth=('neo4j','emma15emma'))
  g.delete_all()
  # loadTeams(g,"./teams.dat")
  # loadGames(g,"./games.dat")
  dupliGames(g,"./teams.dat", "./games.dat")
  print ('Data loaded!')

main()
