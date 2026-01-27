# HBnB Evolution – Part 1 Technical Documentation

This directory contains the technical documentation for the **HBnB Evolution** application, covering the architecture, business logic, and API interactions.

## File Overview

1. **package_diagram.md**  
   - Contains the **High-Level Package Diagram** of the HBnB application.  
   - Illustrates the three-layer architecture (Presentation, Business Logic, Persistence) and the communication via the **Facade pattern**.  
   - Includes explanatory notes about layer responsibilities and the facade design.

2. **business_logic_class_diagram.md**  
   - Contains the **Detailed Class Diagram** for the Business Logic layer.  
   - Shows the main entities: `User`, `Place`, `Review`, and `Amenity`.  
   - Defines attributes, methods, and relationships between classes.  
   - Includes explanations of the entities and their interactions.

3. **sequence_diagrams.md**  
   - Contains **Sequence Diagrams** for four key API calls:  
     1. User Registration  
     2. Place Creation  
     3. Review Submission  
     4. Fetching a List of Places  
   - Demonstrates the flow of interactions across layers (Presentation → Business Logic → Persistence).  
   - Each diagram is accompanied by a detailed explanation.

4. **HBnB_Evolution_Technical_Documentation.md**  
   - **Comprehensive document** compiling all diagrams and explanations.  
   - Serves as a complete blueprint of the system architecture and design.  
   - Can be used as a reference during implementation phases.

## Purpose

This documentation provides:

- A clear understanding of the **system architecture** and design.  
- Visual diagrams to guide **implementation**.  
- Explanations of **entities, relationships, and interactions**.  

It is intended to serve as a **reference for developers**, ensuring consistency and clarity throughout the project.