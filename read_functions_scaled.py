from glycan import glycan
import pandas as pd

def read_egg_data():
    g = glycan()
    # Read data (CSV files) as pandas data frames. Each file is a new line.
    # Note that each file can have multiple experiments, called "tabs" here.
    # You can specify how many tabs you want to read using the totalTabs variable.

    # The "wh" parameter simply controls the format of the CSV file.
    # The 'old' format is slightly different from the 'new' format, but has the same information
    numberedExcel1, b = g.getData('Data/H1N1_EGG/old_sheet1.csv', wh='old', totalTabs=3, startExp=1)
    numberedExcel2, b = g.getData('Data/H1N1_EGG/old_sheet2.csv', wh='old', totalTabs=4, startExp=(b+1))
    numberedExcel3, b = g.getData('Data/H1N1_EGG/old_sheet3.csv', wh='old', totalTabs=4, startExp=(b+1))
    numberedExcel4, b = g.getData('Data/H1N1_EGG/new_sheet1.csv', totalTabs=2, startExp=(b+1))
    numberedExcel5, b = g.getData('Data/H1N1_EGG/new_sheet2.csv', totalTabs=2, startExp=(b+1))
    numberedExcel6, b = g.getData('Data/H1N1_EGG/new_sheet3.csv', totalTabs=2, startExp=(b+1))
    numberedExcel7, b = g.getData('Data/H1N1_EGG/new_sheet4.csv', totalTabs=4, startExp=(b+1))
    numberedExcel8, b = g.getData('Data/H1N1_EGG/new_sheet5.csv', totalTabs=4, startExp=(b+1))
    numberedExcel9, b = g.getData('Data/H1N1_EGG/new_sheet6.csv', totalTabs=4, startExp=(b+1))
    numberedExcel10, b = g.getData('Data/H1N1_EGG/egg_virus_dilutions_secondTab_updated.csv', totalTabs=2, startExp=(b+1))

    # Now combine all the data frames
    numberedExcel_temp = pd.concat([numberedExcel1, numberedExcel2, numberedExcel3, numberedExcel4, numberedExcel5, numberedExcel6, numberedExcel7, numberedExcel8, numberedExcel9, numberedExcel10], axis=0)
    # Removing the blocks with bad data. These were hand-picked by visual inspection of experimental results
    egg = numberedExcel_temp[~((numberedExcel_temp.SubArr == 23) | (numberedExcel_temp.SubArr == 25) | (numberedExcel_temp.SubArr == 26))]
    egg.reset_index(drop=True, inplace=True)
    
    # Reset the -ve fluorescences to 0
    egg.loc[(egg.MVF < 0), 'MVF'] = 0
    
    # Scaling the mean viral fluorescence by glycan density.
    egg['MVF_orig'] = egg['MVF']
    egg['MVF'] = egg.MVF/egg.GlycDen
    return egg


def read_H3N2_data():
    # Create an instance of the glycan class
    g = glycan()

    # Read data (CSV files) as pandas data frames. Each file is a new line.
    # Note that each file can have multiple experiments, called "tabs" here.
    # You can specify how many tabs you want to read using the totalTabs variable.

    # The "wh" parameter simply controls the format of the CSV file.
    # The 'old' format is slightly different from the 'new' format, but has the same information
    numberedExcel1, b = g.getData('Data/H3N2_EGG/H3N2_sheet1.csv', totalTabs=2, startExp=1)
    numberedExcel2, b = g.getData('Data/H3N2_EGG/H3N2_sheet2.csv', totalTabs=2, startExp=(b+1))
    numberedExcel3, b = g.getData('Data/H3N2_EGG/H3N2_sheet3.csv', totalTabs=2, startExp=(b+1))

    # Now combine all the data frames
    h3n2 = pd.concat([numberedExcel1, numberedExcel2, numberedExcel3], axis=0)
    h3n2.reset_index(drop=True, inplace=True)

    # Reset the -ve fluorescences to 0
    h3n2.loc[(h3n2.MVF < 0), 'MVF'] = 0

    # Scaling the mean viral fluorescence by glycan density.
    h3n2['MVF_orig'] = h3n2['MVF']
    h3n2['MVF'] = h3n2.MVF/h3n2.GlycDen
    
    return h3n2



def read_MDCK_data():
    # Create an instance of the glycan class
    g2 = glycan()

    # Read data (CSV files) as pandas data frames. Each file is a new line.
    # Note that each file can have multiple experiments, called "tabs" here.
    # You can specify how many tabs you want to read using the totalTabs variable.
    numberedExcel2, b = g2.getData('Data/H1N1_MDCK/MDCK_sheet2.csv', totalTabs=1, startExp=1)
    numberedExcel3, b = g2.getData('Data/H1N1_MDCK/MDCK_sheet3.csv', totalTabs=1, startExp=(b+1))
    numberedExcel4, b = g2.getData('Data/H1N1_MDCK/MDCK_sheet4.csv', totalTabs=2, startExp=(b+1))

    # Now combine all the data frames
    mdck = pd.concat([numberedExcel2, numberedExcel3, numberedExcel4], axis=0)
    mdck.reset_index(drop=True, inplace=True)

    # Reset the -ve fluorecences to 0
    mdck.loc[(mdck.MVF < 0), 'MVF'] = 0

    # Scaling the mean viral fluorescence by glycan density.
    mdck['MVF_orig'] = mdck['MVF']
    mdck['MVF'] = mdck.MVF/mdck.GlycDen

    return mdck


