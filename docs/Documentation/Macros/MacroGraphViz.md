# GraphViz Macro

This Macro shows how GraphViz generates an image graph from dot file.

## Parameters

The body of the macro is the dot string definition of the graph which will generate a graph image.

## Example
We use the graphviz macro as follows:

    <div class="macro macro_graphviz">
        digraph {

            node [    fill=cornflowerblue,
                      fontcolor=white,
                      shape=diamond,
                      style=filled];

            Step1 [   color=darkgoldenrod2,
                      fontcolor=navy,
                      label=start,
                      shape=box];

            Step2;

            Step3a [  style=filled,
                      fillcolor=grey80,
                      color=grey80,
                      shape=circle,
                      fontcolor=navy];

            Step1  -> Step2;
            Step1  -> Step2a;
            Step2a -> Step3a;
            Step3;
            Step3a -> Step3;
            Step3a -> Step2b;
            Step2  -> Step2b;
            Step2b -> Step3;

            End [ shape=rectangle,
                  color=darkgoldenrod2,
                  fontcolor=navy];

            Step3  -> End [label=193];
            }
    </div>

## Sample

<div class="macro macro_graphviz">
digraph {

  node [    fill=cornflowerblue,
            fontcolor=white,
            shape=diamond,
            style=filled];

  Step1 [   color=darkgoldenrod2,
            fontcolor=navy,
            label=start,
            shape=box];

  Step2;

  Step3a [  style=filled,
            fillcolor=grey80,
            color=grey80,
            shape=circle,
            fontcolor=navy];

  Step1  -> Step2;
  Step1  -> Step2a;
  Step2a -> Step3a;
  Step3;
  Step3a -> Step3;
  Step3a -> Step2b;
  Step2  -> Step2b;
  Step2b -> Step3;
  End [ shape=rectangle,
        color=darkgoldenrod2,
        fontcolor=navy];
  Step3  -> End [label=193];
}
</div>

