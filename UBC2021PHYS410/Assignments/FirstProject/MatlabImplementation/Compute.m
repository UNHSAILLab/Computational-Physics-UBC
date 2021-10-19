function [StarsX, CoresX] = Compute()
    
    tmax = 25;
    l = 10;
    N_timeSteps = 2^l+1;
    
    dt = tmax/(N_timeSteps-1);
    
    NStars1 = 50;
    NStars2 = 5;
    NStars = NStars1 + NStars2;
    NCores = 1;
    
    StarsX = zeros(NStars,3,N_timeSteps);
    CoresX = zeros(NCores,3,N_timeSteps);
    
     StarsV0 = zeros(NStars, 3);
     CoresV0 = zeros(NCores, 3);
     
     StarsTimeCut = zeros(NStars,3);
     CoresTimeCut = zeros(NCores,3);
     
     
     [CoresTimeCut, CoresV0] = initiateCores(CoresTimeCut, CoresV0);
     [StarsTimeCut, StarsV0] = initiateStars(StarsTimeCut, StarsV0, CoresTimeCut, NStars1, NStars2, CoresV0);
%     
%     
%     for t = 1:N_timeSteps
%         
%         for star = 1:NStars
%             StarsX(star,:,t) = rand(1,3);
%         
%         end
% 
%     end
    
     StarsX = initiateFirstTwoSteps(StarsX, StarsTimeCut, StarsV0, dt);
     CoresX = initiateFirstTwoSteps(CoresX, CoresTimeCut, CoresV0, dt);
     
     for t= 2:N_timeSteps
         StarsX = moveStars(StarsX, CoresX, dt,t, NStars, NCores);
         CoresX = moveCores(CoresX, dt,t, NCores);
     
     end
% 
%     fprintf("Calculatoin Done!")
%     


end