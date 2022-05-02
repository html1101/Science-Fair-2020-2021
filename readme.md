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


**How to Run?**

There are a lot 