# SBS BES (**B**eam **E**xtractor and **S**orter)

This is **SBS BES**. It is a Windows executable app built in `Python` that is meant to:
- extract important data from the STAAD syntax (beam groups, beam dimensions, beam names) and STAAD forces file (beam groups, beam forces);
- calculate each beam's **Muneg** (Absolute negative moment), **Mupos** (Absolute positive moment),**Vu** (Shear), and **Tu** (Torsion); and 
- merge all important data into a single `master` table, and writes it into an Excel file.

### Motivation
Over the years, SBStruc has developed a system that optimizes its designs by using custom calculations in Excel in addition to the calculations from STAAD and SPCOL. This results in structural designs that are not only cheaper but also sturdier than those of the competition. However, the manual transfer of data from STAAD to Excel consumes a significant amount of time.
We decided to create **SBS BESI** to solve exactly that. As a result, what used to take atleast **3 hours of manual work can now be completed in as little as 5 minutes**.

--- ADD GIF HERE DEMONSTRATING THE DIFFERENCE BETWEEN THE OLD AND NEW WAY ---


### Quick Start
1. Download the `.exe` file in the releases section. It is a standalone app and no installation is required
> [!Caution]
> If you tried running it and your antivirus software tags it as a virus, do not fret-- that is a false positive. Just add it in the ignore list.
> This program was packages using `PyInstaller` and using it without software signature causes it to get flagged. More explanation [here](https://discuss.python.org/t/pyinstaller-false-positive/43171/12)

2. Get staad syntax from staad
...

3. Copy beam forces in staad syntax and save it as an excel file
...

4. (optional) For SBS engineer, please download the template file. 

5. Click `run`.

### Usage


### Contributing
...
