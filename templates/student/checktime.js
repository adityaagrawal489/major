



function check(start,end){
    var startTime = start;
var endTime   = end;
var now       = new Date();

var startDate = dateObj(startTime); // get date objects
var endDate   = dateObj(endTime);
console.log(startDate);
console.log(endDate)
if (startDate > endDate) { // check if start comes before end
    var temp  = startDate; // if so, assume it's across midnight
    startDate = endDate;   // and swap the dates
    endDate   = temp;
}
var open = now < endDate && now > startDate ? 'open' : 'closed'; // compare
console.log('Restaurant is ' + open);

function dateObj(d) { // date parser ...
    var parts = d.split(/:|\s/),
        date  = new Date();
    if (parts.pop().toLowerCase() == 'pm') parts[0] = (+parts[0]) + 12;
    date.setHours(+parts.shift());
    date.setMinutes(+parts.shift());
    return date;
}
}


sanju=document.querySelectorAll('tr');
sanju.forEach((element,index)=>{
    let start=(element.cells[2].innerHTML);
    let end=(element.cells[3].innerHTML);
    let date=(element.cells[4].innerHTML);
    let today=new Date().toLocaleDateString('en-us', {year:"numeric", month:"long", day:"numeric"});
    if(date===today&&check(start,end)){
        console.log('galat hai')
    }else{
        console.log('sahi hai')
        element.cells[5].hidden=true;

    }
});