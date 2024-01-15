---
title: 'PyRolL - An Extensible OpenSource Framework for Rolling Simulation'
tags:
  - Python
  - Simulation 
  - Groove Rolling
  - Rolling
  - Metal Forming
authors:
  - name: Max Weiner
    email: max.weiner@imf.tu-freiberg.de
    orcid: 0000-0002-8232-6877
    equal-contrib: true
    affiliation: 1

  - name: Christoph Renzing
    email: christoph.renzing@imf.tu-freiberg.de
    orcid: 0000-0002-9250-4358
    equal-contrib: true
    affiliation: 1

  - name: Max Stirl
    email: max.stirl@imf.tu-freiberg.de
    orcid: 0000-0003-3484-9849
    affiliation: 1

  - name: Matthias Schmidtchen
    email: matthias.schmidtchen@imf.tu-freiberg.de
    orcid: 0000-0002-2064-4124
    affiliation: 1

  - name: Ulrich Prahl
    email: ulrich.prahl@imf.tu-freiberg.de
    orcid: 0000-0001-6978-5721
    affiliation: 1


affiliations:
 - name: Institute of Metal Forming, TU Bergakademie Freiberg, Germany
   index: 1
date: 09 October 2023
bibliography: paper.bib

---

# Summary

Groove rolling is one of the main process routes for the production of metal long products, such as bars, beams, wires and rods.
In this process, a workpiece is deformed by two or more rotating rolls to reduce the cross-section achieve a desired cross-section shape.
The shape is determined by the contour of the rolls' surfaces, called the groove or calibre.
The process is usually accomplished in multiple steps, each called a pass.
The industry is currently under heavy pressure to optimize its processes regarding energy consumption while maintaining or increasing product quality.
The introduction of new materials and alloys challenges production and technology engineers.
In the past decades, numerical simulation tools have become an integral part of process development and maintenance.
There are used to estimate forces and engine torques, as well as geometrical and microstructural evolution of the workpiece for a given pass sequence and input workpiece geometry and material.
This knowledge is important to design or optimize a process, identify sources of errors, increase product quality or extend the product portfolio.

PyRolL is an open-source, modular and extensible framework aiming at the numerical simulation of groove rolling processes and accompanying processes, such as heating, cooling and transportation.
PyRolL Core serves as the basis for model and application development by defining needed data structures and solution algorithms and providing a versatile plugin system.
Rolling processes are quite a complex issue since a simulation has to regard the mechanical behavior of the workpiece and plant, as well as thermodynamic and chemical processes occurring within the workpiece.
The plugin system enables modular simulation setup, where the user can choose from a growing library of state-of-the-art model approaches published in scientific literature that target specific aspects of the process auch as material flow, stress state, thermal evolution, microstructure evolution or elastic tool response.
Additional and new model approaches can be implemented as plugin packages and used just the same as officially provided ones.
By this concept, the ecosystem can grow and thus avoid the need to implement the basic stuff every time, so the user or developer can concentrate on the actual focus of his work.

# Statement of need

Established in the late 19th century, mathematical modelling of groove rolling and optimization of used grooves, known as groove or roll pass design, was investigated by a variety of authors.
@Geuze1900, @Brovot1903 and @Mercader1924 gave the first set of rules for the design of grooves as well as simple equations for the calculation of material spread in groove rolling.
Further investigations regarding this topic were carried out by @Siebel1924, who introduced the equivalent rectangle approach to derive the material spread in groove rolling from an equivalent flat roll pass.
This method has been constantly supplemented by various authors [@Lendl1948; @Lendl1948a; @Lendl1949; @Spittel1984; @Lee2000; @Dong2006; @Dong2008].
Furthermore empirical and analytical models have been developed, focusing on different aspects of groove rolling as spreading [@Tafel1925; @Siebel1924; @Ekelund1927; @Roux1939; @Marini1941; @Sparling1961; @Geleji1967; @Wusatowski1969; @Vater1972; @El-Nikhaily1979; @Klasen1984; @Angott1986; @Pawelski1988; @Dixon1996], longitudinal tension [@Treis1968; @Nikkila1977; @Voigtlaender1984; @Schulze1986; @Jaeckel1991; @Lommatzsch1991; @Shokhin2015], strain rate [@Hensel1985], contact area between work roll and rolled stock [@Zouhar1960; @Zouhar1966] and power and work needed [@Zouhar1960; @Zouhar1966; @Hensel1977; @Goldhahn1981; @Hensel1985].
Since 1990, research also focuses on the modelling of microstructure evolution in groove rolling [@Cuong1991; @Lehnert1991; @Lehnert1995a; @Blinov2004; @Krause2007].
Besides the approach of tracing the groove rolling back to an equivalent flat rolling pass, there were also investigations focusing on the modelling of material flow, including the actual shape of the groove [@Hensel1978; @Goldhahn1981; @Hensel1981; @Mauk1982; @Kopp1985; @Hensel1987b].
To make optimum use of these models, attempts to automatic groove pass design were always an issue of development [@Kunzman1977; @Koermer1987; @Hensel1987; @Hensel1987a; @Hensel1988; @Schmidt1997; @Malmgren2000; @Eriksson2004; @Eriksson2004a; @Eriksson2005; @Betshammer2006; @Krause2007; @Lambiase2009; @Alexey2015; @Schmidtchen2020; @Schmidtchen2021; @Overhagen2020; @Overhagen2020a; @Overhagen2021a].
An exhaustive overview of general tasks in roll pass design and published models is given by @Oduguwa2006.

The mentioned models and simulation programs use empirical, analytical or semi-analytical approaches to describe the groove rolling process.
Aside from these models, there is a huge amount of research focusing on the usage of Finite-Element-Method (FEM) based models for groove rolling and groove pass design.
The finite element theory is actively developed since the 1980s for use in groove rolling [@Shivpuri1992; @Macura1996; @Yanagimoto2000; @Liu2002; @Glowacki2005; @Kim2005; @Bontcheva2005; @Vallellano2008; @Bernhardt2013; @Takashima2014].
It provides a general approach for complex problems in two or three dimensions and offers simulation results of high accuracy and depth.
The main disadvantage is the high computational effort in solving the equation systems, increasing rapidly with the non-linearity of the model equations and the resolution of the solution space, typically in the range from hours to days.
Analytical and empirical models, however, do not provide that high accuracy and depth, but are usually computable within fractions of seconds.
So they are suitable for interactive design with quick feedback loops and numerical applications, which require large count of evaluations, such as optimization routines.

According to the authors' experience, it is not common in the field of rolling simulation to provide source code and input files alongside journal publications, so the work cannot be reproduced directly and easily.
Noteable exceptions from this are @Alexander1972 and a textbook by @Pawelski2000.
Also, the field is characterized by the usage of handcrafted, specialized and not reusable self-made tools, or, by the usage of large commercial FE packages, either specialized or general-purpose.
In effect, every research project has to start from scratch to build up a simulation, even if only small partial models have to be investigated.
The authors propose a new open and extensible rolling simulation framework to support future research and development.
The framework is designed to allow a modular exchange of model approaches describing partial problems of the highly complex groove rolling process.
The whole project aims to provide a growing library of model approaches to reflect the state of the art found in scientific literature and make it available to the public.
So new research can start on a growing base to explore the actual topic without implementing the same stuff again and again.
The primary focus lies hereby on analytical, empirical and semi-empirical approaches, although interfacing with third-party software such as FE or CALPHAD suites, as well as material databases, is possible and planned.
PyRolL is deeply integrated with Python's scientific ecosystem, which allows efficient and user-friendly post-processing of simulation results, as well as application of numerical routines wrapped around the simulation core, such as optimization and fitting of metamodels.

# Acknowledgements

The authors thank the following people for their valuable feedback and/or testing efforts:

- Jennifer Mantel (Student, TU Bergakademie Freiberg)
- Richard Pfeifer (Student, TU Bergakademie Freiberg)
- Frank Gerlach (VFUP Riesa e.V.)
- Gerald Rothenbucher (Plansee SE)
- Koos van Putten (SMS Group GmbH)
- Louisa Preis (FNsteel B.V.)
- Christian Overhagen (Universität Duisburg-Essen)
- Tomas Kubina (Liberty a.s.)

The authors thank the following industrial partners for supporting the software development by submitting feedback on usage, simulation result quality and rewarding questions to answer:

- ESF Elbe-Stahlwerke Feralpi GmbH
- FNsteel B.V.
- BGH Edelstahl Freital GmbH
- SMS Group GmbH
- Plansee SE
- Liberty Ostrava a.s.

# Conflict of Interest

The authors declare, that they have no conflict of interest.

# Research Projects

The software development was or is supported by the following research projects:

- Development and Modelling of Wear of Grooved Rolls for Finishing Blocks (Industrial Funding by ESF Elbe-Stahlwerke Feralpi Riesa GmbH)
- Investigations on Material Flow and Forming Conditions (Industrial Funding by ESF Elbe-Stahlwerke Feralpi Riesa GmbH)
- Design and Numerical Investigations of Different Leader Passes for Rebars (Industrial Funding by ESF Elbe-Stahlwerke Feralpi Riesa GmbH)

The software development will be supported by the following coming research projects:

- "Validierungsförderung" by Sächsische Aufbaubank (SAB) and European Union (EU)
- Implementation and Validation of a Calculation Model for Angular Sections produced by Rolling (RISE DAAD)

![](EFRE-ESF_LO_Kombination_EU-Logo_FreistaatSachsen_H_ENG_RGB.png)

# References
