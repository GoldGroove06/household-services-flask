function searchHandler(cond) {
  let search = document.querySelector("#city").value;
  document.querySelector("#searchResult").className = "active";
  if (cond == "serv") {
    searchResultServ(search, cond);
  } else {
    searchResultCust(search, cond);
  }
  if (cond == "prof") {
    pendingHandler(search, cond);
  }
  
}

function searchResultServ(search, cond) {
  console.log(search, cond);
  fetch(`/admin/api/${search}/${cond}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      document.querySelector("#servicesList").innerHTML = "";
      document.querySelector("#packageList").innerHTML = "";

      for (let i = 0; i < data.length; i++) {
        let div = document.createElement("div");
        div.className = "rep-div";
        if (data[i].type == "service") {
          div.innerHTML = ` <div>${data[i].service_name}</div>    <button onclick="deleteServ(${data[i].service_id}, 'service')">Delete</button><button onclick="location.href='/admin/servform/${data[i].service_id}/edit'">Edit</button>`;
          document.querySelector("#servicesList").appendChild(div);
        }
        if (data[i].type == "package") {
          div.innerHTML = ` <div>${data[i].package_name}</div>  <div>₹${data[i].price}</div> <div>${data[i].duration} Hours</div> <button onclick="deleteServ(${data[i].package_id}, 'package')">Delete</button><button onclick="location.href='/admin/pkform/${data[i].package_id}/edit'">Edit</button>`;
          document.querySelector("#packageList").appendChild(div);
        }
        
      }
    });
}


function searchResultCust(search, cond) {
  console.log(search, cond);
  fetch(`/admin/api/${search}/${cond}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      document.querySelector("#active-users").innerHTML = "";
      document.querySelector("#blocked-users").innerHTML = "";
      for (let i = 0; i < data.length; i++) {
        
        if (data[i].status == "active") {
          let div = document.createElement("div");
          div.className = "rep-div";
          div.innerHTML = `<div>${data[i].id}</div>  <div>${data[i].name}</div>  <div>${data[i].email}</div><div>${data[i].mobile}</div> <div>${data[i].address}</div> <div>${data[i].rating}</div> <button onclick=actionHandler('block',${data[i].id})>Block</button> `;
          if (data[i].s_status == "pending") {
              div.innerHTML += `<button onclick='location.href="/admin/verify/${data[i].id}"'>Verify</button>`
          }
          document.querySelector("#active-users").appendChild(div);
        }
        if (data[i].status == "blocked") {
          let div = document.createElement("div");
          div.className = "rep-div";
          div.innerHTML = `<div>${data[i].id}</div>  <div>${data[i].name}</div>  <div>${data[i].email}</div><div>${data[i].mobile}</div> <div>${data[i].address}</div> <div>${data[i].rating}</div> <button onclick=actionHandler('unblock',${data[i].id})>Unblock</button>`;
          document.querySelector("#blocked-users").appendChild(div);
        }
        
      }
    });
}


function actionHandler(action, id) {
  console.log(action, id);
  fetch(`/admin/action/${action}/${id}`, {
    method: "GET",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.m == "success") {
        
        window.location.reload();
      }
    });
}

function deleteServ(id, type) {
  console.log(id);
  fetch(`/admin/manage/serv`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: id,
      type: type,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.m == "success") {
        location.reload();
      }
    });
}  


function newForm(type) {
  const city = document.querySelector("#city").value;
  if (type == "serv") {
  const url = `/admin/servform/${city}/add`;
  location.href = url;
  } 
  if (type == "pk") {
    const url = `/admin/pkform/${city}/add`;
    location.href = url;
  }

}