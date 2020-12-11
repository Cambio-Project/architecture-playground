# Playground for architecture extraction

## model2arch.py
- Takes a MiSim architecture model and stores it in a generic model description
- Can (partially) validate the syntax of a MiSim model  
- Can validate the semantics of a MiSim model (finds undefined operations) 
- Can generate a generic architecture from a generic model description 
- Can validate the semantics of a generic architecture 
    - finds self dependencies 
    - finds cyclic dependencies 
- Can export the architecture to a d3 visualization

![Tests](https://github.com/Cambio-Project/architecture-playground/workflows/Tests/badge.svg)
![Model Test](https://github.com/Cambio-Project/architecture-playground/workflows/Model%20Tests/badge.svg)
![Deploy](https://github.com/Cambio-Project/architecture-playground/workflows/Deploy/badge.svg)

