**SCIENCE FAIR 2020-2021**
Creating Antibodies Using Genetic Algorithms

Steps(Using Javascript):
- Load 4uif.pdb and the FASTA. That will be the PDB(protein data base) file that we will use, as well as the genetic code(which we'll use later; it helps us identify the chains).
This file describes the Dengue virus and the human antibodies surrounding it.
- Now, within application_viewer, do the following:
  - Load OIMO.js and Three.js. OIMO is a wrapper of Three.js that provides a simple physics simulator.
  - Render the antigen molecules described within the .pdb.
  - Find the epitopes - Currently the focus of this project is on forming the antibodies rather than identifying the epitopes, so the epitopes are not the highest priority; right now we are finding for the antibody the closest corresponding antigen values and identifying those as the sections we will suppress. Then we will attach "magnets" to that area such that all randomly produced antibodies are attracted to those points.
  - Work on the genetic algorithm. The fitness function is how well it suppresses the antigen, and each unit within the population will contain a heavy and light chain, just like a normal antibody. The first step will be creating the coordinates, then later the project could use tools such as DeepMind to find the corresponding proteins.