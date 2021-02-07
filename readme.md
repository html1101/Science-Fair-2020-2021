<h1>mRNA Sequence Design Using Optimization Techniques</h1>
<sub>Science Fair 2020-2021</sub>
<hr>

**Current methods:**

- Codon mapping - Mapping the codon values to a lookup table. Simple, quick, and
high nucleotide and codon % matches.
- Discrete optimization version 0:
   - Iterates through and for each codon finds the best optimized codon.
   - Problems with high GC content at beginning and cutting down at end.
   - Slow, relatively good results but not state-of-the-art.
- Discrete optimization version 1:
   - Iterates through, measures fitness within a specific frame(size 12), and for each codon finds best optimized codon.
   - GC content can get extremely close(within 0.1%) to actual vaccine, at cost of major nucleotide and codon differences.
   - Fixes GC problems slightly(although sometimes avg GC content within a specific area might dip, this fixes it so it's not indicative of real vaccine)
- Discrete optimization version 2:
   - Iterates through, measures fitness for entire sequence and finds best codon to change.
   - Very good results - High nucleotide and codon % matches
   - Also high GC % and codon frequency %
   - Much slower than versions 0 and 1
- Discrete optimization version 3:
   - Same as version 2, but optimizes fitness function
   - Converges slightly faster
   - Fitness function normalized and doesn't require alpha value(which is a constant that isn't guaranteed to be the same across different viruses)



SCHEDULE

---------
**Big Dates**

Feb. 7: Scienteer finished

Feb. 13: Slides finished

Feb. 15: Hear from judges

Feb. 20: Presentation


**Todo**
- Find the antigen
  - Given antigen name, isolate it within full genome and run program on it
  - Create lookup table and identify which to use
- Create GA measuring:
  - GC content
  - Codon optimization(looking at frequency of codons in human body & use less rare ones)
  - Hairpin structures
  - CAI Index
- Fix collapsed

**Scienteer Info**
- [x] Title and category
- [x] Team status
- [x] Project start date
- [x] Survey questions
- [x] Research Plan
- [x] Extra Forms
- [x] Bibliography
- [x] Research Locations
- [x] External Signatures
- [x] Project Approval Method
- [x] Teacher Approval
- [x] IRB Approval
- [x] SRC Approval
- [x] Project end date
- [x] 1C Signature
- [x] SRC Post-approval
- [ ] Project Summary
- [ ] Abstract

**Parts**
- [ ] Background
- [x] Rationale
- [ ] Introduction
- [ ] Purpose
- [x] Hypothesis
- [ ] Code
- [x] Procedure
- [x] Materials
- [ ] Conclusion
  - [ ] Problems Encountered
  - [ ] Future Expansions
  - [ ] Practical Applications
- [ ] Bibliography

**Day-by-Day**

Feb. 1
- [x] Research plan
- [x] Extra forms
- [x] Implement CAI index
- [x] Background
- [x] Rationale
- [x] Create vaccine given specific features(codon_mapping.py + identify_antigen.py)

Feb. 2
- [x] Materials
- [x] Implement CAI index

Feb. 3
- [x] Procedure
- [x] GA - Implement mutation, population selection

Feb. 4
- [ ] Problems Encountered
- [ ] Create simple shell script to execute
- [ ] Implement self-replicating vaccine
- [ ] Bibliography
- [ ] Introduction
- [ ] Purpose
- [ ] Background


Feb. 5
- [ ] Future Expansions
- [ ] Practical Applications
- [ ] Implement self-replicating vaccine
- [ ] Apply GA to 3 viruses

Feb. 6
- [ ] Connect self-replicating vaccine to lookup table, find corresponding structural proteins
- [ ] Apply to 3 viruses
- [ ] Calculate when to finish
- [ ] Rendering:
  - [ ] Antigen shading
  - [ ] Run vaccine through AlphaFold + render w/ GFuzz
- [ ] Select best 5' and 3' UTRs + cap
- [ ] Conclusion

Feb. 7
- [ ] Annotate code!
- [ ] Major clean-up of files
- [ ] Continue rendering
- [ ] Conclusion
- [ ] Optimize

Feb. 8
- [ ] Presentation work
- [ ] Continue rendering work
- [ ] Slides
- [ ] Self-replication work

Feb. 9
- [ ] Rendering
- [ ] Presentation
- [ ] Slides
- [ ] Self-replication work

Feb. 10
- [ ] Rendering
- [ ] Apply GA to more viruses
- [ ] Optimize GA if possible
- [ ] Creating UI

Feb. 11
- [ ] Optimize GA
- [ ] Apply GA to more viruses
- [ ] Self-replication work
- [ ] Slides
- [ ] Creating UI

Feb. 11
- [ ] Filler - [ ] Add more info to binder
- [ ] Slides
- [ ] Creating UI

Feb. 12
- [ ] Putting down final results
- [ ] Finalizing slides