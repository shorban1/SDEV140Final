"""

Author:  Seth Horban
Date Last Edited: 12/13/24
Assignment: Final Project
Short Desc:   


"""

#import tkinter library
import tkinter as tk
#from tkinter import messagebox as mb
#import pillow for image capabilities
from PIL import Image, ImageTk
#import fractions for simplification
from fractions import Fraction
#import datetime for file names
import datetime

#class to aid in creating images
#inherits from tk.Label
class ImageLabel(tk.Label):
    #initialixation function - ran upon creation
    def __init__(self, master, phenotype):
        #store a render instance variable in order to keep a reference image with the pillow image
        self.render = ImageTk.PhotoImage(Image.open(pictures[phenotype]).resize((160, 120)))
        #initialize as a label using render as the image
        tk.Label.__init__(self, master, image=self.render)   
    #function to change the image     
    def change_image(self, phenotype):
        #change the render based on the phenotype input
        self.render = ImageTk.PhotoImage(Image.open(pictures[phenotype]).resize((160, 120)))
        #reconfigure the label to use the new render
        self.configure(image=self.render)    

#clears all widgets from frames populated with .pack()
def clear_frame(frame):
    #loop through all packed widgets
    for widget in frame.slaves():
       #clear the current widget
       widget.forget()

def quit_calculator():
    global quit_window, frm_quit, lbl_quit_prompt, btn_quit_yes, btn_quit_no
    quit_window = tk.Toplevel(window)
    quit_window.title("Coturnix Calculator")
    quit_window.resizable(width=False,height=False)

    frm_quit = tk.Frame(master=quit_window)
    lbl_quit_prompt = tk.Label(master=frm_quit, text="Are you sure you want to quit?")
    lbl_quit_prompt.pack()
    btn_quit_yes = tk.Button(master=frm_quit, text="Yes", command=quit_yes)
    btn_quit_yes.pack(side=tk.LEFT, fill=tk.X, expand=True)
    btn_quit_no = tk.Button(master=frm_quit, text="No", command=quit_no)
    btn_quit_no.pack(side=tk.LEFT, fill=tk.X, expand=True)
    frm_quit.pack()

    quit_window.transient(window)
    quit_window.grab_set()
    window.wait_window(quit_window)

    quit_window.mainloop()
    
def quit_yes():
    lbl_quit_prompt.config(text="Would you like to save the results of the current pairing?")
    btn_quit_yes.config(command=quit_save_yes)
    btn_quit_no.config(command=quit_save_no)

def quit_no():
    quit_window.destroy()

def quit_save_yes():
    save_results(lbl_sire_geno["text"], lbl_dam_geno["text"], True)
def quit_save_no():
    window.destroy()

def save_results(sire_geno, dam_geno, destroy=False):
    unique_filename = "CoturnixCalculatorResults_" +str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.') + ".txt"

    file = open(unique_filename, "w")

    file.write("Sire: " + calculate_phenotype(sire_geno) + " | " + sire_geno + "\n")
    file.write("Dam: " + calculate_phenotype(dam_geno) + " | " + dam_geno + "\n")
    file.write("-----------------------------------------------------------------------------------------------\n\n")

    #collect the offspring and frequency list from combination using the parent loci lists
    offspringList, freqList = combinations(sire_geno.split(" "), dam_geno.split(" "))

    file.write("Male Offspring:\n")
    #iterate through each male offspring genotype
    for male_offspring_geno in filter(lambda s: 'Z/Z' in s, offspringList):
        #calculate the probability in both fractional chance and percentage
        percentage = freqList[offspringList.index(male_offspring_geno)] / float(sum(freqList)) * 100
        chance = Fraction(freqList[offspringList.index(male_offspring_geno)], sum(freqList))

        file.write(calculate_phenotype(male_offspring_geno) + " | " + male_offspring_geno + " | " + str(chance) + " = " + str(percentage) + "\n")
    file.write("-----------------------------------------------------------------------------------------------\n\n")
    file.write("Female Offspring:\n")
    #iterate through each male offspring genotype
    for female_offspring_geno in filter(lambda s: 'Z/W' in s, offspringList):
        #calculate the probability in both fractional chance and percentage
        percentage = freqList[offspringList.index(female_offspring_geno)] / float(sum(freqList)) * 100
        chance = Fraction(freqList[offspringList.index(female_offspring_geno)], sum(freqList))

        file.write(calculate_phenotype(female_offspring_geno) + " | " + female_offspring_geno + " | " + str(chance) + " = " + str(percentage) + "\n")
    file.write("-----------------------------------------------------------------------------------------------\n\n")

    global save_window
    save_window = tk.Tk()
    save_window.title("Coturnix Calculator")
    save_window.resizable(width=False,height=False)

    frm_save = tk.Frame(master=save_window)
    lbl_save_prompt = tk.Label(master=frm_save, text="File saved as " + unique_filename)
    lbl_save_prompt.pack()
    btn_save_yes = tk.Button(master=frm_save, text="OK", command=save_ok)
    btn_save_yes.pack()
    frm_save.pack()

    if destroy:
        window.destroy()

    save_window.mainloop()

def save_ok():
    save_window.destroy()

#function to reset the calculator too the initial state 
def reset_calculator():
    #clear all widgets in each offspring frame
    clear_frame(frm_male_offspring)
    clear_frame(frm_female_offspring)
    #replace the heading labels in each offspring frame
    tk.Label(master=frm_male_offspring, text="Male Offspring:").pack()
    tk.Label(master=frm_female_offspring, text="Female Offspring:").pack()

    #reset each allele value to wild type
    sire_locus_E_1_selected.set(value=locus_E[2])
    sire_locus_E_2_selected.set(value=locus_E[2])
    sire_locus_Y_1_selected.set(value=locus_S[1])
    sire_locus_Y_2_selected.set(value=locus_S[1])
    sire_locus_F_1_selected.set(value=locus_F[1])
    sire_locus_F_2_selected.set(value=locus_F[1])
    sire_locus_BR_1_selected.set(value=locus_BR[0])
    sire_locus_BR_2_selected.set(value=locus_BR[0])
    sire_locus_S_1_selected.set(value=locus_S[1])
    sire_locus_S_2_selected.set(value=locus_S[1])
    sire_locus_AL_1_selected.set(value=locus_AL[0])
    sire_locus_AL_2_selected.set(value=locus_AL[0])

    dam_locus_E_1_selected.set(value=locus_E[2])
    dam_locus_E_2_selected.set(value=locus_E[2])
    dam_locus_Y_1_selected.set(value=locus_S[1])
    dam_locus_Y_2_selected.set(value=locus_S[1])
    dam_locus_F_1_selected.set(value=locus_F[1])
    dam_locus_F_2_selected.set(value=locus_F[1])
    dam_locus_BR_1_selected.set(value=locus_BR[0])
    dam_locus_S_1_selected.set(value=locus_S[1])
    dam_locus_S_2_selected.set(value=locus_S[1])
    dam_locus_AL_1_selected.set(value=locus_AL[0])

    #Reset each parent now that the alleles are reset
    sire_calculate_genotype()
    dam_calculate_genotype()

#refreshes the canvas width, placement, and scrollbar functionality
def refresh_canvas():
    #allows for winfo_width() to return current values
    window.update_idletasks() 

    #set the width of the buttons frame to the wild of the canvas content
    new_width = frm_male_offspring.winfo_width() + frm_female_offspring.winfo_width() + frm_offspring_divider.winfo_width()
    frm_buttons.config(width=new_width)

    #center the canvas using the width of its container
    x = frm_offspring_container.winfo_width() / 2
    offspring_canvas.create_window((x, 0), window=frm_offspring, anchor=tk.N)

    #reset the scroll region
    offspring_canvas.configure(scrollregion=offspring_canvas.bbox("all"))

#calculates every possible combination of alleles and loci for two given parent genotypes
#preset with male a female chromosomes and a frequency of two each for each
def combinations(sire_loci, dam_loci, oldList=["Z/Z", "Z/W"], oldFreqList=[2, 2]):
    #initialize empty list that will be used for calculations
    newList = []
    newFreqList = []
    testList = []
    
    #remove and store the first locus in each geno type
    sire_locus = sire_loci.pop(0).split("/")
    dam_locus = dam_loci.pop(0).split("/")

    #runs if the current gene is sex-linked (linked the Z chromosome) by checking for hemizygous state (one allele and the other empty)
    if dam_locus[1] == "-":
        #calculate combinations between each sire allele and the allele of the dam and append exclusively to male genotypes
        for i in sire_locus:
            #run only if the the combination has not already been calculated
            if (i + dam_locus[0]) not in testList:
                #loop through all male genotypes in the oldList
                for geno in filter(lambda s: 'Z/Z' in s, oldList):
                    #append the value to both the test list and new genotype list using the current genotype in the iteration as a basis
                    testList.append(i + dam_locus[0])
                    newList.append(geno + " " + i + "/" + dam_locus[0])
                    #inherit the frequency of the parent genotype
                    newFreqList.append(oldFreqList[oldList.index(geno)])
            #runs if this combination is a repeat
            else:
                #loop through all male genotypes in the oldList
                for geno in filter(lambda s: 'Z/Z' in s, oldList):
                    #add the frequency of the genotype in the old list to that of its child with the repeated locus in the new list
                    newFreqList[newList.index(geno + " " + i + "/" + dam_locus[0])] += oldFreqList[oldList.index(geno)]

#calculate combinations between each sire allele and the empty allele of the dam and append exclusively to female genotypes
        for i in sire_locus:
            #run only if the the combination has not already been calculated
            if (i + "-") not in testList:
                #loop through all female genotypes in the oldList
                for geno in filter(lambda s: 'Z/W' in s, oldList):
                    #append the value to both the test list and new genotype list using the current genotype in the iteration as a basis
                    testList.append(i + "-")
                    newList.append(geno + " " + i + "/-")
                    #inherit the frequency of the parent genotype
                    newFreqList.append(oldFreqList[oldList.index(geno)])
            #runs if this combination is a repeat
            else:
                #loop through all female genotypes in the oldList
                for geno in filter(lambda s: 'Z/W' in s, oldList):                    
                    #add the frequency of the genotype in the old list to that of its child with the repeated locus in the new list
                    newFreqList[newList.index(geno + " " + i + "/-")] += oldFreqList[oldList.index(geno)]
    #runs if the locus is autosomal (2 unlinked alleles)
    else:
        #calculate combinations between each sire allele and each dam allele and append them to every genotype in the old list
        for i in sire_locus:
            for j in dam_locus:
                #run only if the the combination has not already been calculated
                if (i + j) not in testList and (j + i) not in testList:
                    #loop through every genotype in the old list
                    for geno in oldList:
                        #append the value to both the test list and new genotype list using the current genotype in the iteration as a basis
                        testList.append(i + j)
                        newList.append(geno + " " + i + "/" + j)
                        #inherit the frequency of the parent genotype
                        newFreqList.append(oldFreqList[oldList.index(geno)])
                #runs if this combination is a repeat
                else:
                    #loop through every genotype in the old list
                    for geno in oldList:
                        #determine which combination of the current alleles is in the new list
                        if geno + " " + i + "/" + j in newList:
                            #inherit the frequency of the parent genotype
                            newFreqList[newList.index(geno + " " + i + "/" + j)] += oldFreqList[oldList.index(geno)] 
                        else:
                            #inherit the frequency of the parent genotype
                            newFreqList[newList.index(geno + " " + j + "/" + i)] += oldFreqList[oldList.index(geno)]

    #run only if there are more loci (sire is arbitrary, could be dam)
    if len(sire_loci) > 0:
        #rerun the function using the modified loci and new genotype and frequency lists
        return combinations(sire_loci, dam_loci, newList, newFreqList)
    #run if there are no more loci to calculate
    else:
        #return the new genotype and frequency lists
        return newList, newFreqList

#calculates the phenotype based on a genotype
def calculate_phenotype(genotype):
    #remove all wild type loci
    genotype = genotype.replace(" +/+", "").replace(" +/-", "").replace("+/+ ", "")
    #run if the genotype has a phenotype in the dictionary
    if genotype in phenotypes:
        #set the phenotype the the corresponding phenotype in the dictionary
        phenotype = phenotypes[genotype]
    #runs if there is no corresponding phenotype
    else: 
        #set the phenotype to Undefined
        phenotype = "Undefined"
    #return the phenotype
    return phenotype

#function to dynamically change the genotype and phenotype labels of the sire 
#dummy parameter to store unused value given by option menu
def sire_calculate_genotype(dummy=None):
    #strip the gene symbols from the option menus
    e1 = sire_locus_E_1_selected.get().split(" ", 1)[0]
    e2 = sire_locus_E_2_selected.get().split(" ", 1)[0]
    
    y1 = sire_locus_Y_1_selected.get().split(" ", 1)[0]
    y2 = sire_locus_Y_2_selected.get().split(" ", 1)[0]
    
    f1 = sire_locus_F_1_selected.get().split(" ", 1)[0]
    f2 = sire_locus_F_2_selected.get().split(" ", 1)[0]
    
    br1 = sire_locus_BR_1_selected.get().split(" ", 1)[0]
    br2 = sire_locus_BR_2_selected.get().split(" ", 1)[0]
    
    s1 = sire_locus_S_1_selected.get().split(" ", 1)[0]
    s2 = sire_locus_S_2_selected.get().split(" ", 1)[0]
    
    al1 = sire_locus_AL_1_selected.get().split(" ", 1)[0]
    al2 = sire_locus_AL_2_selected.get().split(" ", 1)[0]
    #make a formatted genotype string from the stripped values
    geno = e1 + "/" + e2 + " " + y1 + "/" + y2 + " " + f1 + "/" + f2 + " " + br1 + "/" + br2 + " " + s1 + "/" + s2 + " " + al1 + "/" + al2
    #use the genotype to find the phenotype name
    pheno = calculate_phenotype(geno)
    #update the labels
    lbl_sire_geno["text"] = geno
    lbl_sire_pheno["text"] = pheno
    if pheno in pictures:
        lbl_sire_img.change_image(pheno)
    else:
        lbl_sire_img.change_image("default")

    #reset offspring frames to avoid confusion
    clear_frame(frm_male_offspring)
    clear_frame(frm_female_offspring)
    tk.Label(master=frm_male_offspring, text="Male Offspring:").pack()
    tk.Label(master=frm_female_offspring, text="Female Offspring:").pack()
    #refresh scrolling area
    refresh_canvas()

#function to dynamically change the genotype andphenotype labels of the dam
#dummy parameter to store unused value given by option menu
def dam_calculate_genotype(dummy=None):
    #strip the gene symbols from the option menus
    e1 = dam_locus_E_1_selected.get().split(" ", 1)[0]
    e2 = dam_locus_E_2_selected.get().split(" ", 1)[0]
    
    y1 = dam_locus_Y_1_selected.get().split(" ", 1)[0]
    y2 = dam_locus_Y_2_selected.get().split(" ", 1)[0]
    
    f1 = dam_locus_F_1_selected.get().split(" ", 1)[0]
    f2 = dam_locus_F_2_selected.get().split(" ", 1)[0]
    
    br1 = dam_locus_BR_1_selected.get().split(" ", 1)[0]
    br2 = "-"
    
    s1 = dam_locus_S_1_selected.get().split(" ", 1)[0]
    s2 = dam_locus_S_2_selected.get().split(" ", 1)[0]
    
    al1 = dam_locus_AL_1_selected.get().split(" ", 1)[0]
    al2 = "-"
    #make a formatted genotype string from the stripped values
    geno = e1 + "/" + e2 + " " + y1 + "/" + y2 + " " + f1 + "/" + f2 + " " + br1 + "/" + br2 + " " + s1 + "/" + s2 + " " + al1 + "/" + al2
    #default pheno to "Undefined"
    #use the genotype to find the phenotype name
    pheno = calculate_phenotype(geno)
    #update the labels
    lbl_dam_geno["text"] = geno
    lbl_dam_pheno["text"] = pheno
    #if the phenotype has a corresponding picture
    if pheno in pictures:
        #change the parents image to the corresponding image
        lbl_dam_img.change_image(pheno)
    #if no corresponding image exists
    else:
        #change the parent's image to the default image
        lbl_dam_img.change_image("default")

    #clear offspring frames to avoid confusion
    clear_frame(frm_male_offspring)
    clear_frame(frm_female_offspring)
    tk.Label(master=frm_male_offspring, text="Male Offspring:").pack()
    tk.Label(master=frm_female_offspring, text="Female Offspring:").pack()
    #refresh scrolling area
    refresh_canvas()

#function to run upon clicking calculate
#calculates all combinations using the parent genotypes and outputs all offspring widgets accordingly
def calculate_offspring(sire_geno, dam_geno):
    #transform the parent genotypes into list of loci
    sire_geno = sire_geno.split(" ")
    dam_geno = dam_geno.split(" ")
    #collect the offspring and frequency list from combination using the parent loci lists
    offspringList, freqList = combinations(sire_geno, dam_geno)

    #clear each offspring frame
    clear_frame(frm_male_offspring)
    clear_frame(frm_female_offspring)

    #replace each frames header
    tk.Label(master=frm_male_offspring, text="Male Offspring:").pack()
    tk.Label(master=frm_female_offspring, text="Female Offspring:").pack()
    
    #iterate through each oofspring genotype
    for offspring_geno in offspringList:
        #calculate the probability in both fractional chance and percentage
        percentage = freqList[offspringList.index(offspring_geno)] / float(sum(freqList)) * 100
        chance = Fraction(freqList[offspringList.index(offspring_geno)], sum(freqList))

        #if the genotype is male
        if "Z/Z" in offspring_geno:
            #remove the sex chromosomes from the genotype
            offspring_geno = offspring_geno.replace("Z/Z ", "")
            #find the phenotype based on the genotype
            pheno = calculate_phenotype(offspring_geno)
            #pack the phenotype and the genotype into the male offspring frame
            tk.Label(master=frm_male_offspring, text=pheno).pack()
            tk.Label(master=frm_male_offspring, text=offspring_geno).pack()
            
            #if the phenotype has a corresponding photo
            if pheno in pictures:
                #pack an image into the male offspring frame using the corresponding photo
                ImageLabel(master=frm_male_offspring, phenotype=pheno).pack()
            #omitted for performance
            #if no corresponding photo exists
            #else:
                #pack the default image into the male offspring frame
            #    ImageLabel(master=frm_male_offspring, phenotype="default").pack()

            #pack the fractional and percent chance into the male offspring frame
            tk.Label(master=frm_male_offspring, text=str(chance) + " = " + str(percentage) + "%").pack()
            #pack a divider into the male offspring frame for clarity
            tk.Label(master=frm_male_offspring, text='----------------------------------').pack()
        #if the genotype is female
        elif "Z/W" in offspring_geno:
            #remove the sex chromosomes from the genotype
            offspring_geno = offspring_geno.replace("Z/W ", "")
            #find the phenotype based on the genotype
            pheno = calculate_phenotype(offspring_geno)
            #pack the phenotype and the genotype into the female offspring frame
            tk.Label(master=frm_female_offspring, text=pheno).pack()
            tk.Label(master=frm_female_offspring, text=offspring_geno).pack()

            #if the phenotype has a corresponding photo
            if pheno in pictures:
                #pack an image into the female offspring frame using the corresponding photo
                ImageLabel(master=frm_female_offspring, phenotype=pheno).pack()
            #omitted for performance
            #if no corresponding photo exists
            #else:
                #pack the default image into the female offspring frame
            #    ImageLabel(master=frm_female_offspring, phenotype="default").pack()

            #pack the fractional and percent chance into the female offspring frame
            tk.Label(master=frm_female_offspring, text= str(chance) + " = " + str(percentage) + "%").pack()
            #pack a divider into the female offspring frame for clarity
            tk.Label(master=frm_female_offspring, text='----------------------------------').pack()

    #pack both frames
    frm_male_offspring.grid(row=0, column=0, sticky="NESW")
    frm_female_offspring.grid(row=0, column=2, sticky="NESW")
    #refresh the scroll area
    refresh_canvas()

 
#Option Menu for Locus E
locus_E =["E (Extended Brown)", "Sk (Sparkly)", "+ (Wild Type)"]
locus_Y =["Y (Fawn)", "+ (Wild Type)", "ca (Calico)"]
locus_F =["F (Fee)", "+ (Wild Type)"]
locus_BR=["+ (Wild Type)", "b (Sex-Linked Brown)", "g (Ginger)", "r (Roux)"]
locus_S =["S^DW (Dotted White)", "+ (Wild Type)", "s^S (Splash)"]
locus_AL=["+ (Wild Type)", "al^c (Cinnamon)", "al (Albino)"]

#Dictionary defining each genotype as a phenotype
phenotypes={
    "+/+":"Pharaoh (Wild Type)",

    "E/E": "Tibetan",
    "E/+": "Rosetta",
    "+/E": "Rosetta",
    "E/Sk": "Rosetta",
    "Sk/E": "Rosetta",
    "Sk/Sk": "Sparkly (Homo.)",
    "Sk/+": "Sparkly (Het.)",
    "+/Sk": "Sparkly (Het.)",

    "Y/Y": "Manchurian",
    "Y/+": "Italian",
    "+/Y": "Italian",
    "Y/ca": "Italian",
    "ca/Y": "Italian",
    "+/ca": "Pharaoh",
    "ca/+": "Pharaoh",
    "ca/ca": "Calico",

    "F/F": "Falb Fee",
    "F/+": "Falb Fee",
    "+/F": "Falb Fee",
    "Y/Y F/F": "Perl Fee",
    "Y/Y F/+": "Perl Fee",
    "Y/Y +/F": "Perl Fee",
    "Y/+ F/F": "Perl Fee",
    "Y/+ F/+": "Perl Fee",
    "Y/+ +/F": "Perl Fee",
    "+/Y F/F": "Perl Fee",
    "+/Y F/+": "Perl Fee",
    "+/Y +/F": "Perl Fee",
    "E/E F/F": "Grau Fee",
    "E/E F/+": "Grau Fee",
    "E/E +/F": "Grau Fee",
    "E/+ F/F": "Grau Fee",
    "E/+ F/+": "Grau Fee",
    "E/+ +/F": "Grau Fee",
    "+/E F/F": "Grau Fee",
    "+/E F/+": "Grau Fee",
    "+/E +/F": "Grau Fee",

    "b/b": "Brown",
    "g/g": "Ginger",
    "r/r": "Egyptian",

    "S^DW/S^DW": "English White",
    "+/S^DW": "Pharaoh Tuxedo",
    "S^DW/+": "Pharaoh Tuxedo",
    "s^S/S^DW": "Pharaoh Tuxedo",
    "S^DW/s^S": "Pharaoh Tuxedo",
    "s^S/+": "Pharaoh",
    "+/s^S": "Pharaoh",
    "s^S/s^S": "Pharaoh Splash"
    }
  
pictures={
    "default": "images/default.jpg",

    "Pharaoh (Wild Type)": "images/coturnix-pharaoh-1.jpg",
    "Pharaoh": "images/coturnix-pharaoh-1.jpg",
    "Italian": "images/coturnix-italian-1.jpg"
}

#Configure the window
window = tk.Tk()
window.title("Coturnix Calculator")
window.resizable(width=False,height=False)
window.protocol('WM_DELETE_WINDOW', quit_calculator)


#create frames
frm_container = tk.Frame(master=window)

frm_sire = tk.Frame(master=frm_container, bg="light blue")
frm_dam = tk.Frame(master=frm_container, bg="light blue")
frm_buttons = tk.Frame(master=frm_container)
frm_offspring_container = tk.Frame(master=frm_container)
offspring_canvas = tk.Canvas(master=frm_offspring_container)
offspring_scrollbar = tk.Scrollbar(master=frm_offspring_container, orient=tk.VERTICAL, command=offspring_canvas.yview)
frm_offspring = tk.Frame(master=offspring_canvas)
frm_male_offspring = tk.Frame(master=frm_offspring)
frm_offspring_divider = tk.Frame(master=frm_offspring, bg="black", width=1)
frm_female_offspring = tk.Frame(master=frm_offspring)

#fill the sire frame with its content
lbl_sire = tk.Label(master=frm_sire, bg="light blue", text="Sire")
lbl_sire.grid(row=0, column=0, columnspan=2)
lbl_sire_pheno = tk.Label(master=frm_sire, bg="light blue", text="Pharaoh (Wild Type)")
lbl_sire_pheno.grid(row=1, column=0, columnspan=2)
lbl_sire_geno = tk.Label(master=frm_sire, bg="light blue", text="+/+ +/+ +/+ +/+ +/+ +/+")
lbl_sire_geno.grid(row=2, column=0, columnspan=2)
lbl_sire_img = ImageLabel(master=frm_sire, phenotype="Pharaoh (Wild Type)")
lbl_sire_img.grid(row=3, column=0, columnspan=2)

sire_locus_E_1_selected = tk.StringVar(value=locus_E[2])
opt_sire_locus_E_1 = tk.OptionMenu(frm_sire, sire_locus_E_1_selected, *locus_E, command=sire_calculate_genotype)
opt_sire_locus_E_1.grid(row=4, column=0, sticky="NSEW")
sire_locus_E_2_selected = tk.StringVar(value=locus_E[2])
opt_sire_locus_E_2 = tk.OptionMenu(frm_sire, sire_locus_E_2_selected, *locus_E, command=sire_calculate_genotype)
opt_sire_locus_E_2.grid(row=4, column=1, sticky="NSEW")

sire_locus_Y_1_selected = tk.StringVar(value=locus_S[1])
opt_sire_locus_Y_1 = tk.OptionMenu(frm_sire, sire_locus_Y_1_selected, *locus_Y, command=sire_calculate_genotype)
opt_sire_locus_Y_1.grid(row=5, column=0, sticky="NSEW")
sire_locus_Y_2_selected = tk.StringVar(value=locus_S[1])
opt_sire_locus_Y_2 = tk.OptionMenu(frm_sire, sire_locus_Y_2_selected, *locus_Y, command=sire_calculate_genotype)
opt_sire_locus_Y_2.grid(row=5, column=1, sticky="NSEW")

sire_locus_F_1_selected = tk.StringVar(value=locus_F[1])
opt_sire_locus_F_1 = tk.OptionMenu(frm_sire, sire_locus_F_1_selected, *locus_F, command=sire_calculate_genotype)
opt_sire_locus_F_1.grid(row=6, column=0, sticky="NSEW")
sire_locus_F_2_selected = tk.StringVar(value=locus_F[1])
opt_sire_locus_F_2 = tk.OptionMenu(frm_sire, sire_locus_F_2_selected, *locus_F, command=sire_calculate_genotype)
opt_sire_locus_F_2.grid(row=6, column=1, sticky="NSEW")

sire_locus_BR_1_selected = tk.StringVar(value=locus_BR[0])
opt_sire_locus_BR_1 = tk.OptionMenu(frm_sire, sire_locus_BR_1_selected, *locus_BR, command=sire_calculate_genotype)
opt_sire_locus_BR_1.grid(row=7, column=0, sticky="NSEW")
sire_locus_BR_2_selected = tk.StringVar(value=locus_BR[0])
opt_sire_locus_BR_2 = tk.OptionMenu(frm_sire, sire_locus_BR_2_selected, *locus_BR, command=sire_calculate_genotype)
opt_sire_locus_BR_2.grid(row=7, column=1, sticky="NSEW")

sire_locus_S_1_selected = tk.StringVar(value=locus_S[1])
opt_sire_locus_S_1 = tk.OptionMenu(frm_sire, sire_locus_S_1_selected, *locus_S, command=sire_calculate_genotype)
opt_sire_locus_S_1.grid(row=8, column=0, sticky="NSEW")
sire_locus_S_2_selected = tk.StringVar(value=locus_S[1])
opt_sire_locus_S_2 = tk.OptionMenu(frm_sire, sire_locus_S_2_selected, *locus_S, command=sire_calculate_genotype)
opt_sire_locus_S_2.grid(row=8, column=1, sticky="NSEW")

sire_locus_AL_1_selected = tk.StringVar(value=locus_AL[0])
opt_sire_locus_AL_1 = tk.OptionMenu(frm_sire, sire_locus_AL_1_selected, *locus_AL, command=sire_calculate_genotype)
opt_sire_locus_AL_1.grid(row=9, column=0, sticky="NSEW")
sire_locus_AL_2_selected = tk.StringVar(value=locus_AL[0])
opt_sire_locus_AL_2 = tk.OptionMenu(frm_sire, sire_locus_AL_2_selected, *locus_AL, command=sire_calculate_genotype)
opt_sire_locus_AL_2.grid(row=9, column=1, sticky="NSEW")


#fill the dam frame with its content
lbl_dam = tk.Label(master=frm_dam, bg="light blue", text="Dam")
lbl_dam.grid(row=0, column=0, columnspan=2)
lbl_dam_pheno = tk.Label(master=frm_dam, bg="light blue", text="Pharaoh (Wild Type)")
lbl_dam_pheno.grid(row=1, column=0, columnspan=2)
lbl_dam_geno = tk.Label(master=frm_dam, bg="light blue", text="+/+ +/+ +/+ +/- +/+ +/-")
lbl_dam_geno.grid(row=2, column=0, columnspan=2)
lbl_dam_img = ImageLabel(master=frm_dam, phenotype="Pharaoh (Wild Type)")
lbl_dam_img.grid(row=3, column=0, columnspan=2)

dam_locus_E_1_selected = tk.StringVar(value=locus_E[2])
opt_dam_locus_E_1 = tk.OptionMenu(frm_dam, dam_locus_E_1_selected, *locus_E, command=dam_calculate_genotype)
opt_dam_locus_E_1.grid(row=4, column=0, sticky="NSEW")
dam_locus_E_2_selected = tk.StringVar(value=locus_E[2])
opt_dam_locus_E_2 = tk.OptionMenu(frm_dam, dam_locus_E_2_selected, *locus_E, command=dam_calculate_genotype)
opt_dam_locus_E_2.grid(row=4, column=1, sticky="NSEW")

dam_locus_Y_1_selected = tk.StringVar(value=locus_S[1])
opt_dam_locus_Y_1 = tk.OptionMenu(frm_dam, dam_locus_Y_1_selected, *locus_Y, command=dam_calculate_genotype)
opt_dam_locus_Y_1.grid(row=5, column=0, sticky="NSEW")
dam_locus_Y_2_selected = tk.StringVar(value=locus_S[1])
opt_dam_locus_Y_2 = tk.OptionMenu(frm_dam, dam_locus_Y_2_selected, *locus_Y, command=dam_calculate_genotype)
opt_dam_locus_Y_2.grid(row=5, column=1, sticky="NSEW")

dam_locus_F_1_selected = tk.StringVar(value=locus_F[1])
opt_dam_locus_F_1 = tk.OptionMenu(frm_dam, dam_locus_F_1_selected, *locus_F, command=dam_calculate_genotype)
opt_dam_locus_F_1.grid(row=6, column=0, sticky="NSEW")
dam_locus_F_2_selected = tk.StringVar(value=locus_F[1])
opt_dam_locus_F_2 = tk.OptionMenu(frm_dam, dam_locus_F_2_selected, *locus_F, command=dam_calculate_genotype)
opt_dam_locus_F_2.grid(row=6, column=1, sticky="NSEW")

dam_locus_BR_1_selected = tk.StringVar(value=locus_BR[0])
opt_dam_locus_BR_1 = tk.OptionMenu(frm_dam, dam_locus_BR_1_selected, *locus_BR, command=dam_calculate_genotype)
opt_dam_locus_BR_1.grid(row=7, column=0, sticky="NSEW")
lbl_dam_locus_BR_2 = tk.Label(master=frm_dam, bg="white", text="-")
lbl_dam_locus_BR_2.grid(row=7, column=1, sticky="NSEW")

dam_locus_S_1_selected = tk.StringVar(value=locus_S[1])
opt_dam_locus_S_1 = tk.OptionMenu(frm_dam, dam_locus_S_1_selected, *locus_S, command=dam_calculate_genotype)
opt_dam_locus_S_1.grid(row=8, column=0, sticky="NSEW")
dam_locus_S_2_selected = tk.StringVar(value=locus_S[1])
opt_dam_locus_S_2 = tk.OptionMenu(frm_dam, dam_locus_S_2_selected, *locus_S, command=dam_calculate_genotype)
opt_dam_locus_S_2.grid(row=8, column=1, sticky="NSEW")

dam_locus_AL_1_selected = tk.StringVar(value=locus_AL[0])
opt_dam_locus_AL_1 = tk.OptionMenu(frm_dam, dam_locus_AL_1_selected, *locus_AL, command=dam_calculate_genotype)
opt_dam_locus_AL_1.grid(row=9, column=0, sticky="NSEW")
lbl_dam_locus_AL_2 = tk.Label(master=frm_dam, bg="white", text="-")
lbl_dam_locus_AL_2.grid(row=9, column=1, sticky="NSEW")


#fill the buttons frame with its contents
btn_calc = tk.Button(master=frm_buttons, text="Calculate", bg="navy", fg="white", command=lambda: calculate_offspring(lbl_sire_geno["text"], lbl_dam_geno["text"]))
btn_calc.pack(fill=tk.X)

btn_reset = tk.Button(master=frm_buttons, text="Save", bg="navy", fg="white", command=lambda: save_results(lbl_sire_geno["text"], lbl_dam_geno["text"]))
btn_reset.pack(side=tk.LEFT, fill=tk.X, expand=True)

btn_reset = tk.Button(master=frm_buttons, text="Reset", bg="navy", fg="white", command=reset_calculator)
btn_reset.pack(side=tk.LEFT, fill=tk.X, expand=True)

btn_quit = tk.Button(master=frm_buttons, text="Quit", bg="navy", fg="white", command=quit_calculator)
btn_quit.pack(side=tk.LEFT, fill=tk.X,expand=True)

lbl_male_offspring = tk.Label(master=frm_male_offspring, text="Male Offspring:")
lbl_male_offspring.pack()
lbl_female_offspring = tk.Label(master=frm_female_offspring, text="Female Offspring:")
lbl_female_offspring.pack()

frm_male_offspring.grid(row=0, column=0, sticky="NESW")
frm_offspring_divider.grid(row=0, column=1, sticky="NESW", padx=20)
frm_female_offspring.grid(row=0, column=2, sticky="NESW")


#put the frames within the window in grid format to display their contents

frm_offspring.pack(fill=tk.X, expand=True)
offspring_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
offspring_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

frm_sire.grid(row=0, column=0, sticky="NESW")
frm_dam.grid(row=0, column=1, sticky="NESW")
frm_buttons.grid(row=1, column=0, columnspan=2, sticky="NESW")
frm_offspring_container.grid(row=2, column=0, columnspan=2, pady=20, sticky="NESW")

frm_container.pack()

#set up scrolling functionality
offspring_canvas.configure(yscrollcommand=offspring_scrollbar.set)

# Calculate the coordinates for centering frame in canvas
window.update_idletasks() 
x = frm_offspring_container.winfo_width() / 2
offspring_canvas.create_window((x, 0), window=frm_offspring, anchor=tk.N)

#initialize the window for event listening
window.mainloop()