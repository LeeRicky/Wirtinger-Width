# Wirtinger Width

This code is used to calculate upper bounds on the [Wirtinger width](https://arxiv.org/abs/1912.02295) of knot diagrams.

## Description

Wirtinger width is a reformulation of Gabai width (for details, see my linked paper above). The process of calculating Wirtinger width
on a knot diagram is algorithmic. Our program takes advantage of this to calculate the Gabai width from the [Gauss code](http://katlas.org/wiki/Gauss_Codes_) 
of a knot diagram.

On all knots we tested so far, we depend on the fact that the knots are prime and have bridge number 4.

The excel files organize knots by their crossing number and whether they are alternating. So 13a_ww gives the Gauss codes and Wirtinger 
width of all the 13 crossing alternating knots we tested. 13n_ww gives the Gauss codes and Wirtinger width of all the 13 crossing 
non-alternating knots we tested.

The outline of our program is as follows:

1. Extract the strand and crossing information from our Gauss code.
2. Derive knot dictionary from our Gauss code.
3. Pick 3 strands of our diagram D.
4. Extend the three seeds strands using coloring moves as much as possible.
5. If we get a multi-colored crossing, then verify that our initial 3 strands is a part of a completed coloring sequence. This is done
by adding 1 more strand as a seed strand, and seeing if we can completely color the entire knot diagram using only coloring moves. If
we are successful, then the Wirtinger width is 28.
6. If we don't get a multi-colored crossing or if we fail step 5, then repeat step 3 with all combinations of 3 strands. Repeat until
we return 28 in step 6. If we fail for all combinations of step 3, then Wirtinger width is 32.

Note our implementation currently relies heavily on the fact that our knots are prime and have bridge number 4. This is because for such
knots, Gabai width can only be 28 or 32. Wirtinger width is equivalent to Gabai width so each time our code outputs 28, we know we 
actually calculated the Gabai width of that knot. However, if our code outputs 32, then we have only calculated an upper bound on Gabai
width.

Our code calculated width 28 on 54756 of the knots we tested.


## Acknowledgments

* This code is an adaptation of [this](https://github.com/pommevilla/calc_wirt/blob/master/calc_wirt.py) program, which calculates 
a similar invariant called the [Wirtinger number](https://arxiv.org/abs/1705.03108). The functions used to create knot_dictionary 
were taken directly from the program calc_wirt.py in the linked project. 


