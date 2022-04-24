import numpy as np



class Patient:

    def __init__(self):

        lambda_rel = 2
        lambda_intern = 1
        lambda_phys = 7.23 * 1e-5
        k_on = 0.04 / 0.5
        k_off = 0.04

        H = 0.1                                 ## Hematocrit [1]
        BW = 80                                 ## Body weight [kg]
        gender = "male"                         ## male of female
        BSA = 1.94                              ## Body Surface Area [m^2]

        V_body = BW * 1000                      ## Based on 1g==1ml assumption
        V_tu = 0.087                            ## litre
        V_L = 1.811                             ## litre
        V_S = 0.198                             ## litre
        V_K = 0.193                             ## litre

        R_tu_density = 15                       ## nmol/L
        R_L_density = 1.4                       ## nmol/L
        R_S_density = 8.7                       ## nmol/L
        R_K_density = 6.5                       ## nmol/L
        R_rest_density = 0.5                    ## nmol/L

        lambda_rel_NT = 0.7 * 1e-4              ## 1/min
        lambda_rel_TU = 1.1 * 1e-4              ## 1/min

        tumorType = "NET"                       # NET or MEN
        f_tu = 0.1 * 0.001                      # L/min/g
        k_pr = 4.7 * 1e-4                       # 1/min
        GFR = 0.11                              # L/mi

        k = 0.02                                ## L/min/kg | for muscle | --> please see the important note bellow. In a nutshell, /kg is the right unit here

        ## Important Note: In the table of Frenco 2021 paper, the units of k_i are in ml/min/g which is in fact
        ## the permeability surface area product per unit mass of organ. In order to get the permeability of the
        ## organ we need to multipy k_i at the mass of organ (1gr = 1ml). So the calculated PS value will be:
        ## PS = 1000 * k * V  (Note that V is in Litre). So PS will have the units of ml/min. Now to get the standard
        ## units of (L/min) we need to multiply it at 0.001. So PS with standard units (L/min) will be: PS = k*V

        if gender == "male":
            V_p = 2.8 * (1 - H) * BSA           ## Volume of total body serum
        else:
            V_p = 2.4 * (1 - H) * BSA           ## Volume of total body serum

        #F = 1.23 * V_p



        if tumorType == "NET":
            v_tu_int = 0.3
            v_tu_v = 0.1
            k_tu = 0.2  ## for PS calculation ## L/min/Kg (See the comment in Data.py file under MuscleData
        else:
            v_tu_int = 0.23
            v_tu_v = 0.11
            k_tu = 0.31  ## for PS calculation  ## L/min/Kg (See the comment in Data.py file under MuscleData

        lambda_rel_tu = 1.5 * 1e-4
        lambda_intern_tu = 0.001


        # self.Tumor = {
        #     "name": "Tumor",
        #     "F": f_tu*(1-H)* V_tu,
        #     "PS": k_tu*V_tu,
        #     "V_total": V_tu,
        #     "V_v": 1,
        #     "V_int": v_tu_int * V_tu,
        #     "k_on": k_on,
        #     "k_off": k_off,
        #     "lambda_intern": lambda_intern_tu,
        #     "lambda_rel": lambda_rel_tu,
        #     "lambda_phys": lambda_phys,
        #     "R0": R_tu_density * V_tu,
        #     "K_on": 0, ## R*k_on
        # }

        self.Tumor = {
            "name": "Tumor",
            "F": 5.0,
            "PS": 1.0,
            "V_total": 2,
            "V_v": 1,
            "V_int": 1,
            "k_on": 1.0,
            "k_off": 0.5,
            "lambda_intern": 0.5,
            "lambda_rel": 0.05,
            "lambda_phys": 0.1,
            "R0": 10,
            "K_on": 0,  ## R*k_on
        }
        self.Tumor['K_on'] = self.Tumor["R0"] * self.Tumor["k_on"]

        self.org2 = {
            "name": "org2",
            "F": 1,
            "PS": 1,
            "V_total": 2,
            "V_v": 1,
            "V_int": 1,
            "k_on": 0,
            "k_off": 1,
            "lambda_intern": lambda_intern,
            "lambda_rel": lambda_rel,
            "lambda_phys": lambda_phys,
            "R0": 0,
            "K_on": 0,  ## R*k_on
        }

        self.Kidney = {
            "name": "Kidney",
            "F": 2,
            "V_total": 2,
            "V_v": 1,
            "V_int": 1,
            "V_intra": 1,
            "k_on": 10,
            "k_off": 5,
            "lambda_intern": 0.5,
            "lambda_rel": 0.1,
            "lambda_phys": 0.1,
            "R0": 10,
            "K_on": 0,  ## R*k_on
            "phi": 1.1002,
            "GFR":  1,
            "f_exc": 1,
            "F_fil": 0,     ## F_filtration = GFR * phi
            "F_R": 0,       ## F_Return = F_fill - F_exc = GFR * phi * (1-f_exc)
        }
        self.Kidney["F_fil"] = self.Kidney["GFR"] * self.Kidney["phi"]
        self.Kidney["F_R"] = self.Kidney["F_fil"] * (1-self.Kidney["f_exc"])

        self.Lungs = {
            "name": "Lungs",
            "F": 0,  # The real value will be calculated once we have the
            ## the flow of each organ. The Vein and Art flow is the sum of all flows
            "PS": 1.0,
            "V_total": 2.0,
            "V_v": 1,
            "V_int": 1,
            "lambda_phys": 1.0,
        }

        self.Skin = {
            "name": "Skin",
            "F": 1,
            "PS": 1,
            "V_total": 2,
            "V_v": 1,
            "V_int": 1,
            "lambda_phys": 0.1,
        }


        # V_vein = (0.18 + 0.045) * V_p
        # self.Vein = {
        #     "name": "Vein",
        #     "F": 0, ## The real value will be calculated once we have the
        #     ## the flow of each organ. The Vein and Art flow is the sum of all
        #     ## flows
        #     "V_v": V_vein,
        #     "lambda_phys": lambda_phys,
        # }
        #
        # V_art = (0.06 + 0.045) * V_p
        # self.Art = {
        #     "name": "Art",
        #     "F": 0,  ## The real value will be calculated once we have the
        #     ## the flow of each organ. The Vein and Art flow is the sum of all flows
        #     "V_v": V_art,
        #     "lambda_phys": lambda_phys,
        # }

        V_vein = 1
        self.Vein = {
            "name": "Vein",
            "F": 0,  ## The real value will be calculated once we have the
            ## the flow of each organ. The Vein and Art flow is the sum of all
            ## flows
            "V_v": V_vein,
            "lambda_phys": 0.1,
        }

        V_art = 1
        self.Art = {
            "name": "Art",
            "F": 0.0,  ## The real value will be calculated once we have the
            ## the flow of each organ. The Vein and Art flow is the sum of all flows
            "V_v": V_art,
            "lambda_phys": 0.1,
        }


        V_lungs_total = 1 * BW/71           ## [L]
        V_lungs_v = 0.105 * V_p             ## [L]
        alpha_lungs = 5.5                   ## interestitial to vascular ratio

        # self.Lungs = {
        #     "name": "Lungs",
        #     "F": 0,  # The real value will be calculated once we have the
        #     ## the flow of each organ. The Vein and Art flow is the sum of all flows
        #     "PS": k * V_lungs_total,
        #     "V_total": V_lungs_total,
        #     "V_v": V_lungs_v,
        #     "V_int": alpha_lungs * V_lungs_v,
        #     "lambda_phys": lambda_phys,
        # }



        self.receptorPositiveList = [self.Tumor]
        self.KidneyList = [self.Kidney]
        self.receptorNegativeList = [self.Skin]
        self.calculateTotalF()
        self.ArtVeinList = [self.Art, self.Vein]

        self.calculateK_on()    ## Will calculate K_on = k_on * R0 for RecPos and Kidney
        self.Organs = {
            "ArtVein": self.ArtVeinList,
            "Lungs": [self.Lungs],
            "RecNeg": self.receptorNegativeList,
            "RecPos": self.receptorPositiveList,
            "Kidney": self.KidneyList,
        }


    def calculateK_on(self):
        for elem in self.receptorPositiveList:
            elem["K_on"] = elem["k_on"] * elem["R0"]
        for elem in self.KidneyList:
            elem["K_on"] = elem["k_on"] * elem["R0"]

    def calculateTotalF(self):
        F = 0.0
        for elem in self.receptorNegativeList:
            F += elem['F']
        for elem in self.receptorPositiveList:
            F += elem['F']
        for elem in self.KidneyList:
            F += elem["F"]

        self.Art['F'] = F
        self.Vein['F'] = F
        self.Lungs["F"] = F