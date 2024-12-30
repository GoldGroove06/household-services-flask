function popSearchHandler(search) {
    document.querySelector(".dropdown").value = search
    searchHandler()
}


function searchHandler() { 
    console.log(document.querySelector(".dropdown").value);
    let search = document.querySelector(".dropdown").value
    document.querySelector("#pop-div").className = "inactive";
    document.querySelector("#searchDiv").className = "active";
    searchResult(search)
}

function searchResult(search) {
    fetch(`/search/${search}`,{
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        

        document.querySelector("#searchResult").innerHTML = ""
        document.querySelector("#searchResult").innerHTML = '<div class="ser-pack"><div >Package Name</div>  <div >Duration</div> <div >Price</div>    <div style="flex:0"></div>  </div>'

        for (let i = 0; i < data.length; i++) {
            let div =  document.createElement("div")
            div.className = "ser-pack"
            div.innerHTML = ` <div >${data[i].package_name}</div>  <div >${data[i].duration} Hours</div> <div >₹${data[i].price}</div>  <button  onclick="location.href='/book/${data[i].package_id}'">Book</button>`
            document.querySelector("#searchResult").appendChild(div)
        }
        
        })
    
}