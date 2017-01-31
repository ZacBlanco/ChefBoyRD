function [orders] = gen_data(days, cph, day_offset, noise)
% Function res_data
%
% This function generates multiple tables based on the sample restaurant
% data sceme which can be found at
% http://www.databaseanswers.org/data_models/restaurant_bookings/index.htm
%
% Inputs:
%   days (int) - number of days of transactions to generate
%   cph (int) - daily average of customers per hour to generate
%   day_offset (int) - the number of days after today to begin simulation
%   noise (float) - A number between 0 and 1 representing the range of
%   noise allowed on our values
%
% Outputs
%   bookings - a table with the following columns in order
%           [ year, month, day, dotw, hour, booking_id, num_people ]
%    orders - a table with the following items in order
%           [ year, month, day, dotw, hour, num_people, num_items, total_price ]
%
%

% Restaurant hours range from 0700 to 2200
%
num = 1;
orders = zeros(days*cph*17, 8);
for d = 0:days
    % Create orders
    td = today('datetime') + d + day_offset;
    wkdy = weekday(td);
    for i = 1:(cph*17) % 14 is num of hours opened
        hour = gethr(noise);
        ppl = getppl(noise);
        nd = ndishes(ppl, noise);
        price = price(nd, noise);
        orders(num,:) =  [td.Year, td.Month, td.Day, wkdy, hour, ppl, nd, price];
        num = num + 1;
    end

end


end

function d = getday(offset)
d = round(today('datenum') - (2017*365.243)) + offset;
end

function hr = gethr(noise)
hrpdf = makedist('Poisson', 'lambda', 12 + normrnd(0, 1.5*noise));
hr = mod(random(hrpdf), 15) + 7;
end

function ppl = getppl(noise)
pplpmf = makedist('normal', 'mu', 3, 'sigma', 1+noise);
ppl = round(random(pplpmf)) + 1;
end

function n = ndishes(ppl, noise)
    n = abs(round(normrnd(0, 1+noise))) + ppl;
end

 function tp = price(dishes, noise)
     tp = 0;
     for n = 1:dishes
         tp = tp + round(normrnd(14, 6)) + normrnd(1, noise);
     end
     tp = 1.15*tp; %add the tip
 end





