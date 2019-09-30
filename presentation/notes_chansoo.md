# 1. What are Graphs?

# 2. History

# 3. Use Cases

- Airports
	- Here's a really pretty network visualization, which shows an attempt to show the network behind air transport
	- It has 3275 airports and 37153 routes based on OpenFlights.org data. 
	- The author here used a force-directed graph drawing algorithm to reveal the geographic clustering that we would expect to see. So an example of a force-directed algorithm is one that uses repulsive forces between nodes and attractive forces between adjacent nodes, trying to reach a aesthetically pleasing result. 
	- So a question may be which airports are most important to maintain efficiency in the air travel network? If we had to pick one to repair and update to significantly reduce delay time, which one should we pick?

- Entity Resolution

- Multilayer Networks
	- Another powerful way that newtorks can be used is to aggregate multiple heterogeneous data sources
	- In the most basic sense, think about a network of tweets, retweets, and mentions. You might want to treat each of these connections differently.
	- But another example might be in the representation of different modes of transport in a city such as subways, buses, trains, and so on. 
	- And there have been studies where researchers found nodes in networks that are not particularly interesting in a monolayer network, but can be critical in a multilayer network. 

# 4. Algorithms

- Pathfindings

- Centrality
	
	- Centrality algorithms are useful to identify the most "important" nodes, where "important" could mean most connected, central, influential, and so on. Examples of centrality algorithms include Degree Centrality, Closeness Centrality, Betweenness Centrality, and Eigenvector Centrality. Given one of these algorithms, you can compute the centrality measure for each node in your network.  
	- Example:
		- Eigenvector Centrality
			- Eigenvector centrality computes the centrality for a node based on the centrality of its neighbors. And the centrality of these neighbors are also dependent upon the centrality of their neighbors -- and so on.
			- And as this notion suggests, the eigenvector centrality is defined recursively.
			- Without going into the matrix algebra to show how you can compute the measures, I have a little visualization here that helps to understand the intuition. 
			- On the left you have a small graph where nodes are colorcoded based on degree centrality. Darker nodes are more important.
			- On the right nodes are colorcoded based on eigenvector centrality.
			- In both graphs, the node in the center has outward paths to 4 nodes, where as the node in the bottom only has three.
			- So based on degree centrality, 4 is greater than 3 and thus, the node in the center has the highest measure. 
			- However, based on eigenvector centrality, we don't just care who you influence but how influential are the people you have influenced? The node in the center has influenced four nodes but they are all terminal. They have not influenced any others. But for the node in the bottom, it has influenced the node in the center, which has influenced four other nodes. So the node in the bottom gets the higher measure of eigenvector centrality. 

- Community Detection

# 5. Graphs in Python: NetworkX

# 6. Schools

- Data Source
	- the Mathematics Genealogy Project (https://genealogy.math.ndsu.nodak.edu/) collects information on math, computer science, statistics academics, including when and where they got their PhD and when and where their students got their PhDs
	- can we use this information to spot trends in the movements of academics between universities (e.g. PhD from university A, advised students at university B)
	- can we use this information to rank schools' graduate math programs?
- Show Graph and Summary Statistics (Whole Graph + Subsets)
- Explain Nodex + Edges (properties)
- Hierarchy of Schools + Change Over Time
	- Eigenvector Centrality
- Community Detection

# 7. Conclusions

