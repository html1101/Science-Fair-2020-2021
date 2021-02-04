<h1>mRNA Sequence Design Using Genetic Optimization</h1>

<sub>Science Fair 2020-2021</sub>

<hr>

Pfizer Vaccine Ingredients:

Contains tozinamaran, intramuscular injection

Nucleoside-modified mRNA

Need to be stored between -90 and -60C until 5 days before vaccination

10 Jan 2020 - SARS CoV-2 genetic sequences were released by the Chinese Center for Disease Control and Prevention

Two doses given 3 weeks apart

- mRNA

- lipids(protect mRNA and provide exterior to help mRNA enter cells)

  - ((4-hydroxybutyl)azanediyl)bis
  
    - (hexane-6,1-diyl)bis(2-hexyldecanoate),
  
    - 2 [(polyethylene glycol)-2000]-N
  
    - N-ditetradecylacetamide,
  
    - 1,2-Distearoyl-sn-glycero-3-
  
  phosphocholine

  - cholesterol
  
  - Salts(balances acidity in body)

  - Potassium chloride
  
    - Monobasic potassium phosphate
  
    - Sodium chloride
  
    - Dibasic sodium phosphate dihydrate
  
  - Sucrose



BNT162b2 - encodes prefusion stabilized membrane-anchored SARS-CoV-2 full length spike(one selected for emergency use by FDA)

  - a lipid nanoparticle-formulated, nucleoside-modified RNA vaccine
  
  BNT162b1 - encodes secreted trimerized SARS-CoV-2 receptor-binding domain

Spike N501Y substitution(mutations in S glycoproteins) is a PROBLEM(the UK and South Africa varient) because it's located in the viral receptor binding site for cell entry, increases binding to receptor (angiotensin converting enzyme 2)

angiotensin converting enzyme 2 - Enzyme attached to cell membranes of cells located in lungs, heart, kidney, and intestines.



reverse genetic system - An approach to discovering the function of a gene by analyzing the phenotypic effects of specific gene sequences obtained by DNA sequencing.





Studies were:

- Multinational

- Placebo-controlled

- Observer-blinded

- Pivotal efficacy trials



Lipid nanoparticles are good carriers because:

- Protect mRNA construct as it travels through the bloodstream

- Helps it cross cell membrances and get from the blood into its destination.



DNA is stable, but RNA just has to get into the cell to encounter its site of action(ribosomes). DNA has to get into the nucleus, and that's another membrane to cross. DNA can also get mistakenly incorporated into a cell's own genome.



Antibody starts producing SARS-CoV-2 Spike proteins in large enough quantities that the immune system freaks out, and gives it enough signs that the cells have been taking over.



Start: cap GA - tells cell the code is coming from the nucleus(which makes it think it's ligit)

Reading begins at 5' or five-prime beginning, ends at 3' or three-prime ending.



Ψ technique - Calms immune system while being accepted as U in relevant parts of the system.

mRNA degrades quickly, so the cell could not replicate with it.



Ribosome - translate RNA into proteins, ingests a strand of RNA and emits a strand of amino acids which fold into proteins



How to evade detection:

- Ψ technique

Increasing mRNA stability: https://www.nature.com/articles/s41598-019-42509-y



Main goal of vaccine: Teaches the immune system what the virus looks like, which allows the immune system to vigorously attack the actual virus if it enters the body.

Virus - made of DNA or RNA wrapped in a coat of proteins

Making the coat of protein - make mRNA, which makes the proteins. mRNA of a specific structure makes a protein of a specific structure.



precision in antigen design, good tolerability, and broad immune responses with a highly scalable manufacturing platform



AlphaFold - Folding protein problem using neural networks



Functions of proteins are defined by their 3D structures.

Spike proteins - Allows virus to enter our cells

Determining protein structures through X-ray crystallography, nuclear magnetic resonance, and cryo-electron microscopy

Look at clusters of proteins with similar amino acid sequences = similar structure(MSA)



Current Work:

- Taking sample HG00239 from https://www.internationalgenome.org/data-portal/sample, converting CRAM to FASTA format through samtools(http://www.htslib.org/doc/samtools-fasta.html)

- Running AlphaFold to fold a given sequence, putting it through CWView, converting it from CASP RR format using GFuzz3D(http://genesilico.pl/gdserver/GDFuzz3D/help.html) and superimposing it onto the actual protein to compare performance





https://www.frontiersin.org/articles/10.3389/fimmu.2019.00594/full

Advances in mRNA Vaccines for Infectious Diseases

Save $$$

Could be used for cancer(prophylactic tool - prevent disease) and elimination of allergens

Before: inactivated vaccines produced by chemical or heat treatment and usually involved animals or unfavorable growth condutions

Live attenuated vaccines - LAV, weaken disease-causing pathogens under laboratory conditions

CD8+ cells - cells that induce cell death(aptosis), presents antigen on MHC class I

MHC - major histocompatibility complex, genes that code for proteins found on surfaces of cells, help ilicit immune system response

Problems: could cause disease in immuno-compromised people and through back-mutation(reverts back) could become virulent, mutations, or recombination with wild-type strains

Overall: Subunit and peptide vaccines(mimic naturally occuring proteins from pathogens) aren't as effective(large scale protein expression dissiculties, protein purities from lack of microorganism compatibility, stability issues), elicit a robust CD8+ immune response





Parts:

- UTR - untranslated region

- Cap - Kinda like a header in coding lingo

- Starts with "GA" - like executable #!

- Marks code as coming from the nucleus(it's not)

- ORF - 5' untranslated region, ex kozak sequence(A/GCCAUGG) makes protein production efficient, houses start codon

- 3' untranslated region allows for stability of mRNA and increased protein translation(through natural degregation of the sequence)

- UTR also give metadata about when translation should happen and how much, for Pfizer used slightly modified alpha globin gene

- "They found that the mRNA from the murine Rps27a gene showed the highest translation capacity per mRNA molecule." For 5' UTRs, best was S27a-44'(https://www.scienceboard.net/index.aspx?sec=sup&sub=bioproc&pag=dis&ItemID=1282)



Parameters:

- Eliminate rare codons

- GC content

- RNA secondary structure

- Cleavage sites

- Restriction endonuclease sites

- Added or deleted motifs



mRNA:

- Codon optimization avoids rare codons with low utilization to increase protein production, efficiency, mRNA abundance and stability. Endogenous genes with frequent codons have high protein expression levels. Less common codons: https://www.genscript.com/tools/codon-frequency-table

- CAI - Codon adaptation index, problems are coding sequence becomes one amino acid - one codon where CAI=1.0, overexpression of gene can lead to depletion of the tRNAs resulting in tRNA pool impabalance and an increased likelyhood in translational errors. 

- Sequence optimization and usage of modified nucleosides

- 100% of codons with GC at third position provided better mRNA stablity, processing, and nucleocytoplasmic transport(https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5000471/)

- Incorporating modified nucleosides, ex. pseudouridine(Ψ), 5-methlcytidine(5 mC), cap-1 structure and optimized codons

- Thermostable vaccines - freeze-dried mRNA with trehalose or naked mRNA, expressed high levels of proteins and was associated with higher immunity levels in newborns and elderly(https://doi.org/10.2144/000112593)

- Recognition from innate immune receptors because sequence and secondary structures from mRNA are typically recognized can be fixed with sequence optimization and usage of modified nucleosides

- Protamine-encapsulated vaccine w/ oscillating temperatures between 4 and 56C didn't change immunogenicity effects, though 

- Cationic liposome and cell penetrating peptide(CPP) protected mRNA from degregation by RNase



Lipid nanoparticles?

- HIV big intravenous challenge, mRNA encoding light and heavy chansin of neutralizing anti-HIV antibody encapsulated in lipid nanoparticles helped protect micr from HIV challenge

- Helped avoid limitation of toxic chemical transfection reagents by being based on modified cationic lipid or lipid polymers

- Enhances antigen expression

- Facilitate delivery of RNA

- Can be used as platform to deliver mRNA vaccines against HIV-1 by subcutaneous route which elicited CD4 and CD8 T cell response, or through intranasal route, which induced antigen-specific immune response

- LNP + nucleoside modification = more efficate



Influenza virus

- Used S-adenosylmethionine on methylated capped RNA(cap-0) to make cap-1 to increase mRNA translation efficiency



- Viruses: HIV, cytomegalovirus(CMV), human papiloma virus

Cancer?

- Typically used as therapeutic and not as prophylactic

- Express tumor-associated antigens that stimulate cell-mediated immune responses to clear or inhibit cancer cells



Two forms of mRNA vaccines: conventional and self-amplifying mRNA vaccines derived from positive strand RNA viruses(ssRNA viruses, viral mRNA that can be directly translated into proteins rather than viral RNA complementary to viral mRNA)

- Before 1995 and Ross we didn't like mRNA because of its fragility, small-scale production, and omnipresent ribonucleases

- mRNA can not be synthetically produced through cell-tree enzymatic transcription reaction



Conventional mRNA

- ORF for target antigen

- UTRs and terminal poly(A) tail



Self-amplifying mRNA

- saRNA vaccines - genetically engineered replicons from self-replicating single-stranded RNA viruses

- Structural protein sequences replaced with gene of interest(GoI) and resulting genome is called a replicon, mimics production of antigens by viral pathogens.

- Higher antigen levels

- Amplified by encoding RNA-dependent RNA polymerase

- Derived from Sindbis virus, Semliki Forest virus, Kunjin virus, et cetera

- Does not have viral structural proteins so replicon doesn't produce infectious viral particles



Safe?

- Yes!

- Potential to be much safer

- Cannot integrate into host genome

- Degrade naturally during process of antigen expression

- Degrade before process of cell replicating



Steps:

- Let's start with COVID. The biggie.

- Let's split up the genome

  - CDS - coding sequence, region of DNA translated to form proteins, ORF might contain introns but CDS refers to concatenated exons that can be divided into codons and translated into amino acids.
  
    - mat_peptides - Bunch of peptides.
  
    - ORIGIN - the stuff we're really looking at.
  
  

https://www.biorxiv.org/content/10.1101/640862v1.full.pdf

Hairpin structures



https://www.mdpi.com%2F1422-0067%2F21%2F14%2F5130%2Fpdf&usg=AOvVaw07nbYvSySfHgyg85Ayxzja

antigen focus



Sources:

https://berthub.eu/articles/posts/reverse-engineering-source-code-of-the-biontech-pfizer-vaccine/

https://blog.jonasneubert.com/2021/01/10/exploring-the-supply-chain-of-the-pfizer-biontech-and-moderna-covid-19-vaccines/

https://www.fda.gov/media/144414/download

https://www.nejm.org/doi/10.1056/NEJMoa2027906

https://www.mcmasteroptimalaging.org/full-article/plus/safety-efficacy-bnt162b2-mrna-covid-19-vaccine-96137

https://www.biorxiv.org/content/10.1101/2021.01.07.425740v1.full

https://berthub.eu/articles/posts/part-2-reverse-engineering-source-code-of-the-biontech-pfizer-vaccine/

https://www.ncbi.nlm.nih.gov/nuccore/MT072688

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1463026/

https://www.health.harvard.edu/blog/why-are-mrna-vaccines-so-exciting-2020121021599

https://towardsdatascience.com/alphafold-2-explained-a-semi-deep-dive-fa7618c1a7f6

https://www.ncbi.nlm.nih.gov/Taxonomy/taxonomyhome.html/index.cgi?chapter=cgencodes#SG1

https://deepmind.com/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology

https://www.predictioncenter.org/casp13/index.cgi?page=format#RR

http://genesilico.pl/gdserver/GDFuzz3D/help.html

Pietal, M.J., Bujnicki, J.M. and Kozlowski, L.P., 2015. GDFuzz3D: a method for protein 3D structure reconstruction from contact maps, based on a non-Euclidean distance function. Bioinformatics, 31(21), pp.3499-3505.

Schenck, Ryan O. and Lakatos, Eszter and Gatenbee, Chandler and Graham, Trevor A. and Anderson, Alexander R. A. NeoPredPipe: high-throughput neoantigen prediction and recognition potential pipeline. BMC Bioinformatics. 2019. 20:264. https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-2876-4

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7766040/

https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-2876-4#Sec2

https://www.frontiersin.org/articles/10.3389/fimmu.2019.01424/full

https://bmccancer.biomedcentral.com/articles/10.1186/s12885-018-4325-6

http://biopharm.zju.edu.cn/tsnadb/

https://neofox.readthedocs.io/en/latest/02_installation.html

http://www.htslib.org/doc/samtools-fasta.html

https://www.nature.com/articles/s41598-020-77466-4

https://bmcsystbiol.biomedcentral.com/articles/10.1186/1752-0509-6-134

https://www.nature.com/articles/s41598-020-74091-z

https://www.biorxiv.org/content/10.1101/640862v1.full.pdf

https://www.hindawi.com/journals/jir/2017/2680160/

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC340524/pdf/nar00247-0410.pdf

