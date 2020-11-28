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

![Blank](https://github.com/Cambio-Project/architecture-playground/.github/workflows/test.yml/badge.svg)
![Blank](https://github.com/Cambio-Project/architecture-playground/.github/workflows/test_misim.yml/badge.svg)
![Blank](https://github.com/Cambio-Project/architecture-playground/.github/workflows/deploy_misim.yml/badge.svg)

[Deployed MiSim Architecture](https://cambio-project.github.io/architecture-playground/graph.html)

```
# MiSim architecture model

# Structure of a dependency
Dependency:
    - service: str
    - operation: str
    - probability: float

# Structure of an operation
Operation:
    - name: str
    - demand: int
    - dependencies: [Dependency]
    - circuitBreaker
        - rollingWindow: int
        - requestVolumeThreshold: int
        - errorThresholdPercentage: float
        - timeout: int
        - sleepWindow: int

# Structure of a service
Service:
    - name: str
    - instances: int
    - capacity: int
    - operations: [Operation]
    - patterns: [?]

# Top level property of the MiSim architecture model
- microservices : [Service]
```

```
# MiSim experiment model

# Structure of a generator
Generator:
    - microservice: str
    - operation: str
    - interval: float

# Structure of a chaosmonkey
Chaosmonkey:
    - microservice: str
    - instances: int
    - time: int

# Top level properties of the MiSim experiment model
- simulation_meta_data
    - experiment_name: str
    - model_name: str
    - duration: int
    - report: str
    - datapoints: int
    - seed: int
- request_generators: [Generator]
- chaosmonkeys: [Chaosmonkey]
```
