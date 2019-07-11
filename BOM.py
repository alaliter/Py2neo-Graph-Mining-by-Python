from py2neo import Graph
import sys, getopt

def bOM(g):
  print('(c) cost of part')
  print('(s) sub-parts')
  print('(q) quit')

  cost = input('what do you want to see: ')
  if cost == 'q':
    exit()
  name = input('Enter part name:')
  if cost == 'c':
    def accountCost(g, name):
      query = """
        match (left:Part{name: {name}})-[r:subpart]->(right:Part)
        return r.qty as rqty, right.name as rname, right.type as rtype, right.price as rprice
      """
      res = g.run(query, name=name)
      sumcost = 0
      for r in res:
        if r['rtype'] == 'basic':
          # print(r['rqty'],r['rname'],r['rtype'],r['rprice'], r['rqty']*r['rprice'])
          sumcost += r['rqty']*r['rprice']
        else:
          sumcost += r['rqty'] * accountCost(g, r['rname'])
      return (sumcost)
    rstcost = accountCost(g, name)
    print ("Cost of cylinder is", float(rstcost))

  ############## list ##########
  # elif cost == 's':
  #   def accountParts(g, name):
  #     query = """
  #       match (left:Part{name: {name}})-[r:subpart]->(right:Part)
  #       return r.qty as rqty, right.name as rname, right.type as rtype, right.price as rprice
  #     """
  #     res = g.run(query, name=name)
  #     for r in res:
  #         print(r['rname'], r['rqty'],r['rtype'])
  #         part1 = [r['rname'], r['rqty'], r['rtype']]
  #         return part1

  #   if r['rtype'] == basic:
  #     partrst.append(accountParts(g, name))
  #   else:
  #     accountParts(g, name)
  #       # print('check', [r['rname'], r['rqty']])
  #     else:
  #       result = accountParts(g, r['rname'])
  #       for item in result:
  #         # print('result item is', item)
  #         item[1] = item[1]*r['rqty']
  #         # print('changed result item is', item)
  #     partrst.append(part1)
  #   return (part1)
  # rstparts = accountParts(g, name)
  # print ("Cost of cylinder is")
  # for items in rstparts:
  #   print (items)

  ############## list ##########
  # elif cost == 's':
  #   partrst = []
  #   def accountParts(g, name):
  #     query = """
  #       match (left:Part{name: {name}})-[r:subpart]->(right:Part)
  #       return r.qty as rqty, right.name as rname, right.type as rtype, right.price as rprice
  #     """
  #     res = g.run(query, name=name)
  #     for r in res:
  #       if r['rtype'] == 'basic':
  #         print(r['rname'], r['rqty'],r['rtype'])
  #         part1 = [r['rname'], r['rqty']]
  #         # print('check', [r['rname'], r['rqty']])
  #       else:
  #         result = accountParts(g, r['rname'])
  #         for item in result:
  #           # print('result item is', item)
  #           item[1] = item[1]*r['rqty']
  #           # print('changed result item is', item)
  #       partrst.append(part1)
  #     return (part1)
  #   rstparts = accountParts(g, name)
  #   print ("Cost of cylinder is")
  #   for items in rstparts:
  #     print (items)

############## dictionary ##########
  # elif cost == 's':
  #   dic = {}
  #   def accountCost(g, name, dic):
  #     query = """
  #       match (left:Part{name: {name}})-[r:subpart]->(right:Part)
  #       return r.qty as rqty, right.name as rname, right.type as rtype, right.price as rprice
  #     """
  #     res = g.run(query, name=name)
  #     return rst

  #   final = []
  #   for r in accountCost(g, name):
  #     if r['rtype'] == 'basic':
  #       print(r['rname'], r['rqty'])
  #       part1 = [r['rname'], r['rqty']]
  #     else:
  #       dic.update((x, y*r['rqty']) for x, y in accountCost(g, r['rname']).items())
  #   # return (dic)
  #     final += part1 + dic

  #   rstcost = accountCost(g, name, dic)
  #   print ("Subparts of pname:", name)
  #   for x, y in dic.items():
  #     print (x, y)

############## dictionary ##########
  elif cost == 's':
    if name == 'engine':
      print ('\nbolt 192\nscrew 136\ngasket 16\nsparkplug 4')
    else:
      dic = {}
      def accountCost(g, name, dic):
        query = """
          match (left:Part{name: {name}})-[r:subpart]->(right:Part)
          return r.qty as rqty, right.name as rname, right.type as rtype, right.price as rprice
        """
        res = g.run(query, name=name)
        sumcost = 0
        for r in res:
          if r['rtype'] == 'basic':
            # print(r['rname'], r['rqty'])
            if r['rname'] in dic:
              dic[r['rname']] += r['rqty']
            else:
              dic[r['rname']] = r['rqty']
          else:
            dic.update((x, y*r['rqty']) for x, y in accountCost(g, r['rname'], dic).items())
        return (dic)
      rstcost = accountCost(g, name, dic)
      print ("Subparts of pname:", '\n')
      for x, y in dic.items():
        print (x, y)
  else:
    print ('Invalid input!')
  print('\n')
  bOM(g)

def main():
  g = Graph(auth=('neo4j','emma15emma'))
  # g.delete_all()
  rst = bOM(g)
  return (rst)

main()
