"""

Author:  Seth Horban
Date written: 11/26/24
Assignment:   Module 6 Assignment Part 1
Short Desc:   This is a simple temperature converter. An entry box is 
    used to take in values and there are two buttons: one converts the 
    temperature to celsius as if it were fahrenheit and the other does 
    the converse. The result is then displayed next to the entry with
    the corresponding unit.


"""

#import tkinter library
import tkinter as tk

#function to dynamically change the genotype andphenotype labels of the sire 
#dummy parameter to prevent errors when using command
def sire_calculate_genotype(dummy):
    #strip the gene symbols from the option menus
    e1 = sire_locus_E_1_selected.get().split(" ", 1)[0]
    e2 = sire_locus_E_2_selected.get().split(" ", 1)[0]
    #make a formatted genotype string from the stripped values
    geno = e1 + "/" + e2
    #use the genotype to find the phenotype name
    pheno = phenotypes[geno]
    #update the labels
    lbl_sire_geno["text"] = geno
    lbl_sire_pheno["text"] = pheno

#function to dynamically change the genotype andphenotype labels of the dam
#dummy parameter to prevent errors when using command
def dam_calculate_genotype(dummy):
    #strip the gene symbols from the option menus
    e1 = dam_locus_E_1_selected.get().split(" ", 1)[0]
    e2 = dam_locus_E_2_selected.get().split(" ", 1)[0]
    #make a formatted genotype string from the stripped values
    geno = e1 + "/" + e2
    #default pheno to "Undefined"
    #use the genotype to find the phenotype name
    pheno = "Undefined"
    pheno = phenotypes[geno]
    #update the labels
    lbl_dam_geno["text"] = geno
    lbl_dam_pheno["text"] = pheno


#Configure the window
window = tk.Tk()
window.title("Coturnix Calculator")

#create frames
frm_sire = tk.Frame(master=window)
frm_dam = tk.Frame(master=window)
frm_buttons = tk.Frame(master=window)
frm_results = tk.Frame(master=window)

#Option Menu for Locus E
locus_E =["E (Extended Brown)", "Sk (Sparkly)", "e+ (Wild Type)"]
#Dictionary defining each genotype as a phenotype
phenotypes={
    "e+/e+":"Pharoah (Wild Type)", 
    "E/E": "Tibetan", 
    "E/e+": "Rosetta", 
    "e+/E": "Rosetta", 
    "E/Sk": "Rosetta", 
    "Sk/E": "Rosetta", 
    "Sk/Sk": "Sparkly (Homo.)",
    "Sk/e+": "Sparkly (Het.)", 
    "e+/Sk": "Sparkly (Het.)"
    }

#fill the sire frame with its content
lbl_sire = tk.Label(master=frm_sire, text="Sire")
lbl_sire.grid(row=0, column=0, columnspan=2)
lbl_sire_pheno = tk.Label(master=frm_sire, text="Pharoah (Wild Type)")
lbl_sire_pheno.grid(row=1, column=0, columnspan=2)
lbl_sire_geno = tk.Label(master=frm_sire, text="e+/e+")
lbl_sire_geno.grid(row=2, column=0, columnspan=2)
sire_locus_E_1_selected = tk.StringVar(value=locus_E[2])
opt_sire_locus_E_1 = tk.OptionMenu(frm_sire, sire_locus_E_1_selected, *locus_E, command=sire_calculate_genotype)
opt_sire_locus_E_1.grid(row=3, column=0)
sire_locus_E_2_selected = tk.StringVar(value=locus_E[2])
opt_sire_locus_E_2 = tk.OptionMenu(frm_sire, sire_locus_E_2_selected, *locus_E, command=sire_calculate_genotype)
opt_sire_locus_E_2.grid(row=3, column=1)


#fill the dam frame with its content
lbl_dam = tk.Label(master=frm_dam, text="Dam")
lbl_dam.grid(row=0, column=0, columnspan=2)
lbl_dam_pheno = tk.Label(master=frm_dam, text="Pharoah (Wild Type)")
lbl_dam_pheno.grid(row=1, column=0, columnspan=2)
lbl_dam_geno = tk.Label(master=frm_dam, text="e+/e+")
lbl_dam_geno.grid(row=2, column=0, columnspan=2)
dam_locus_E_1_selected = tk.StringVar(value=locus_E[2])
opt_dam_locus_E_1 = tk.OptionMenu(frm_dam, dam_locus_E_1_selected, *locus_E, command=dam_calculate_genotype)
opt_dam_locus_E_1.grid(row=3, column=0)
dam_locus_E_2_selected = tk.StringVar(value=locus_E[2])
opt_dam_locus_E_2 = tk.OptionMenu(frm_dam, dam_locus_E_2_selected, *locus_E, command=dam_calculate_genotype)
opt_dam_locus_E_2.grid(row=3, column=1)

#fill the buttons frame with its contents
btn_calc = tk.Button(master=frm_buttons, text="Calculate")
btn_calc.pack()

#put the frames within the window in grid format to display their contents
frm_sire.grid(row=0, column=0, sticky="NESW")
frm_dam.grid(row=0, column=1, sticky="NESW")
frm_buttons.grid(row=1, column=0, columnspan=2, sticky="NESW")
frm_results.grid(row=2, column=0, columnspan=2, sticky="NESW")

#initialize the window for event listening
window.mainloop()