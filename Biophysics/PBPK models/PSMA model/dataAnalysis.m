nParams = 2; % two free parameters: repeatInterval X n_repeat
nParam1 = 8; % number of elements for different repeatInterval values
nParam2 = 10; % number of elements for differnet n_repeat values
nTINvalues = 5; % number of TIN values calculated. This include:
%SpleenTIN, KidneyTIN, LiverTIN, RedMarrowTIN, TumorTIN

% converting the "Scenario" table format to meshgrid format
paramMesh = reshape(data1.samples.generate{:,:},nParam1,nParam2,nParams);
paramMesh = pagetranspose(paramMesh);
% paramMesh is equal to meshgrid(param1Range, param2Range)

TINvalues = zeros(nParam1*nParam2, nTINvalues);

for i = 1:nParam1*nParam2
    TINvalues(i,:) = data1.results(i).ScalarObservables{:,:};
end


% I wrote the following two lines intuitivley. I need to evaluate its
% conrrectness more rigrously.
TINvaluesMesh = reshape(TINvalues,nParam1,nParam2,nTINvalues);
TINvaluesMesh = pagetranspose(TINvaluesMesh);

contourf(paramMesh(:,:,1), paramMesh(:,:,2), TINvaluesMesh(:,:,2))

