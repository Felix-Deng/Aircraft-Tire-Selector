# Manufacturer Data 

To test and validate our program, we retrieved aircraft tire engineering data from Michelin Aircraft Tire. 

Specifically, we focused on two types of tires: 
- [Bias type VII tires, presented with the three part (inch code) nomenclature](#bias-type-vii--three-part-inch-code)
- [Radial civil tires, presented with the three part (inch code) nomenclature](#radial-civil-three-part-inch-code)

All nomenclatures are also explained with dimensions shown on the cross-sectional plot of an inflated tire [below](#inflated-tire-dimensions-at-rated-tire-pressure). 

## Bias Type VII + Three Part (Inch Code)
The file `bias_tire_data.csv` is prepared with column names using the "Notation" column from the table below. 

| Category | Name | Unit | Notation | 
| :------- |:---- | :--- | :------- | 
| Tire Descriptions | Prefix | | Pre |
| | Nominal Overall Diameter | in. | M |
| | Nominal Section Width | in. | N |
| | Rim Diameter | in. | D |
| | Ply Rating | | PR |
| | Speed Index | mph (or knot if otherwise specified with "kt") | SI |
| Application Rating | Max. Loading | lbs | Lm |
| | Inflation Pressure (Unloaded) | psi | IP |
| | Approx. Bottoming Load | lbs | BL |
| Inflated Tire Dimensions | $D_o$ Max. | in. | DoMax|
| | $D_o$ Min. | in. | DoMin |
| | $W$ Max. | in. | WMax |
| | $W$ Min. | in. | WMin |
| | $D_s$ Max. | in. | DsMax |
| | $W_s$ Max. | in. | WsMax |
| Aspect Ratio | | | AR |
| Static Loaded Radius | At Rated Load | in. | LR_RL|
| | At Bottoming Load | in. | LR_BL |
| Rim Description | Width Between Flanges | in. | A |
| | Specified Rim Diameter | in. | RD |
| | Flange Height ($F_H$) | in. | FH |
| | Min. Ledge Width | in. | G |
| | Outer Flange Diameter ($D_F$) | in. | DF |
| Qualification Standard | | | QS |
| | | | |

Notes: 
- The Three Part Nomenclature in tire descriptions may contain a prefix designation by B, C, H, or *. 
- \* in tire description prefix: this dimensional data for this size was defined in metric units which, for consistency, has been converted to english units.

## Radial Civil Three Part (Inch Code)
The file `radial_tire_data.csv` is prepared with column names using the "Notation" column from the table below. 

| Category | Name | Unit | Notation | 
| :------- |:---- | :--- | :------- | 
| Tire Descriptions | Prefix | | Pre |
| | Nominal Overall Diameter | in. | M |
| | Nominal Section Width | in. | N |
| | Rim Diameter | in. | D |
| | Ply Rating | | PR |
| | Speed Index | mph | SI |
| Application Rating | Max. Static Load | lbs | Lm |
| | Inflation Pressure (Unloaded) | psi | IP |
| Inflated Tire Dimensions | $D_G$ | in. | DG|
| | $W_G$ | in. | WG |
| | $D_{SG}$ Max. | in. | DSG |
| | $W_{SG}$ Max. | in. | WSG |
| Aspect Ratio | | | AR |
| Grown Static Loaded Radius | Max. | in. | LR_max|
| | Min. | in. | LR_min |
| Rim Description | Width Between Flanges | in. | A |
| | Specified Rim Diameter | in. | RD |
| | Flange Height ($F_H$) | in. | FH |
| | Min. Ledge Width | in. | G |
| | Outer Flange Diameter ($D_F$) | in. | DF |
| Qualification Standard | | | QS |
| | | | |

## Inflated tire dimensions (at rated tire pressure)

![Alt text](tire_dimension.png)

- \* $D_O$: Outside Diameter
- \*\* $D_G$: Maximum Grown Overall Diameter
- \* $W$: Cross Section Width
- \*\* $W_G$: Maximum Grown Section Width
- \* $D_S$: Shoulder Diameter
- \*\* $D_{SG}$: Maximum Grown Shoulder Diameter
- \* $W_S$: Shoulder Width
- \*\* $W_{SG}$: Maximum Grown Shoulder Width
- \* $H$: Section Height
- \* $H_S$: Shoulder Height
- $A$: Width between Rim Flanges
- $D$: Specified Rim Diameter
- $F_H$: Rim Flange Height
- $D_F$: Rim Flange Diameter

Notes: 
- \*: Dimensions of new, unused inflated tire (after 24 hours) 
- \*\*: Dimensions of new, grown inflated tire (after 50 TSO take-off cycles).

Special designations: 
- B tires have a rim width to tire section ratio of 60% to 70% and a 15° bead taper.
- H type tires are the same, except they have a 5° bead taper.
- Standard deflections for B and H type tires is 35% +1,-4
- The C designates a cantilever type tire. It has a very narrow rim width, a section ratio less than 60% and a 15° bead taper.