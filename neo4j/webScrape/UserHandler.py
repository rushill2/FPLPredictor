from  neo4j import GraphDatabase
from WebScraper import *

# server connection link
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "cs411fpl"))
username = 'rushill'
playername = 'Harry Kane'
varray = []

# adds a user node
def add_user(driver, uname):
    with driver.session() as session:
        q0 = "CREATE CONSTRAINT ON (u) ASSERT u.uname IS UNIQUE"
        # session.run(q0)
        q1 = "CREATE (u:User) SET u.uname= $uname"
        session.run(q1, uname=uname)
        # removes duplicate nodes
        query_ = "MATCH (u:User { uname: $uname}) WITH u SKIP 1 DELETE u"
        session.run(query_, uname=uname)
    

# Adds a player with a given name to the node, and creates a IN_TEAM relationship
def add_plyr(driver, pname, uname):
    with driver.session() as session:
        q2 = "CREATE CONSTRAINT ON (p) ASSERT p.pname IS UNIQUE"
        # session.run(q2)
        q4 = "CREATE (p:Player) SET p.pname = $pname, p.uname = $uname"
        session.run(q4, pname=pname, uname=uname)
        session.run("MATCH (p:Player { pname: $pname}) WITH p SKIP 1 DETACH DELETE p", pname=pname)  
        session.run("MATCH (p:Player),(u:User) WHERE u.uname = p.uname AND p.pname = $pname MERGE (p)-[r:IN_TEAM_OF]->(u)", pname=pname)
        # session.run("MATCH (p:Player { uname: $uname})-[r:IN_TEAM_OF]->(u:User) WITH p, u, r SKIP 1 DELETE r;", uname=uname)          
        # add_newsnode(driver, pname)

#call in add player
def add_newsnode(driver_, pname):
    titlelist.clear()
    desclist.clear()
    linklist.clear()
    scrape(pname)
    # print(titlelist)
    namesplit = playername.split(' ', 2)
    first = namesplit[0]
    last = namesplit[1]
    # print(titlelist, desclist, linklist)
    with driver.session() as session:
        ctr = 0
        for title_ in titlelist:
            if ctr==4:
                break
            desc_ = desclist[ctr]
            link_ = linklist[ctr]
            query1 = "CREATE (n:News) SET n.title_ = $title_, n.desc_ = $desc_, n.link_ = $link_"
            session.run(query1, title_=title_, desc_=desc_, link_=link_)
            query2 = "MATCH (n:News),(p:Player) WHERE p.pname = $pname OR n.title_ CONTAINS p.pname OR n.title_ CONTAINS $last OR n.title_ CONTAINS $first MERGE (n)-[:NEWS_FOR]->(p)"
            session.run(query2, pname=pname, last=last, first=first, desc_=desc_, link_=link_)
            ctr+=1
                
        # deletes nodes with no matches
        session.run("MATCH (n) WHERE size((n)--())=0 DELETE (n)")
        session.run("MATCH (n)-[r:NEWS_FOR]->(p) WHERE NOT(n.title_ CONTAINS p.pname) DELETE r")
        session.run("MATCH (n)-[r:NEWS_FOR]->(p) WHERE NOT(n.title_ CONTAINS p.pname) DELETE n")


        # deletes duplicate nodes
        # session.run("MATCH (n:News) WITH n.title_ AS title, COLLECT(n) AS nodelist, COUNT(*) AS count WHERE count > 1 CALL apoc.refactor.mergeNodes(nodelist) YIELD node RETURN node")

plyr_list = []

def del_node(driver, type_, name):
    with driver.session() as session:    
    
            # if type_ == 'user':
            #     uname = name
            #     q7 = "MATCH (u:User { uname: $uname }) DETACH DELETE u"
            #     session.run(q7, uname=uname)

            # elif type_ == 'player':
            #     pname = name
            #     q7 = "MATCH (p:Player { pname: $pname }) DETACH DELETE p"
            #     session.run(q7, pname=pname)
                
            # elif type_ == 'news':
            #     title_ = name
                q7 = "MATCH (n) DELETE n"
                session.run(q7, name=name)
        
# del_node(driver, 'player', playername)
# del_node(driver, 'user', username)
del_node(driver, 'news', playername)

# add_user(driver, username)
# add_plyr(driver, playername, username)
# add_newsnode(driver, playername)
driver.close()

