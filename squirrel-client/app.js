var editId = null;

var dialog = document.querySelector("#squirrel-dialog");
var dialogTitle = document.querySelector("#dialog-title");
var nameInput = document.querySelector("#squirrel-name-input");
var sizeInput = document.querySelector("#squirrel-size-input");
var addButton = document.querySelector("#add-button");
var saveButton = document.querySelector("#save-button");
var cancelButton = document.querySelector("#cancel-button");

addButton.onclick = function () {
  dialog.style.display = "block";
  dialogTitle.innerHTML = "Add Squirrel";
  nameInput.value = "";
  sizeInput.value = "";
  editId = null;
};

saveButton.onclick = function () {
  saveSquirrelOnServer();
};

cancelButton.onclick = function () {
  dialog.style.display = "none";
};

function loadSquirrelsFromServer() {
  dialog.style.display = "none";

  fetch("http://localhost:8080/squirrels").then(function (response) {
    response.json().then(function (data) {
      console.log("Data received from server:", data);

      var squirrelsList = document.querySelector("#squirrels-list");
      squirrelsList.innerHTML = "";

      data.forEach(function (squirrel) {
        var newListItem = document.createElement("li");

        var nameDiv = document.createElement("div");
        nameDiv.innerHTML = squirrel.name;
        nameDiv.classList.add("name");
        newListItem.appendChild(nameDiv);

        var sizeDiv = document.createElement("div");
        sizeDiv.innerHTML = squirrel.size;
        sizeDiv.classList.add("size");
        newListItem.appendChild(sizeDiv);

        var editButton = document.createElement("button");
        editButton.classList.add("fa");
        editButton.classList.add("fa-pencil");
        editButton.onclick = function () {
          dialog.style.display = "block";
          dialogTitle.innerHTML = "Edit Squirrel";
          nameInput.value = squirrel.name;
          sizeInput.value = squirrel.size;
          editId = squirrel.id;
        };
        newListItem.appendChild(editButton);

        var deleteButton = document.createElement("button");
        deleteButton.classList.add("fa");
        deleteButton.classList.add("fa-trash");
        deleteButton.onclick = function () {
          if (confirm("Are you sure you want to delete " + squirrel.name + "?")) {
            deleteSquirrelFromServer(squirrel.id);
          }
        };
        newListItem.appendChild(deleteButton);

        squirrelsList.appendChild(newListItem);
      });
    });
  });
}

function saveSquirrelOnServer() {
  // prepare data to send to the server:
  // e.g. name=Chippy&size=small
  var data = "name=" + encodeURIComponent(nameInput.value);
  data += "&size=" + encodeURIComponent(sizeInput.value);
  console.log("Data to be sent to server:", data);

  var path = "/squirrels";
  var method = "POST";
  if (editId) {
    path += "/" + editId;
    method = "PUT";
  }

  fetch("http://localhost:8080" + path, {
    method: method,
    body: data,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  }).then(function (response) {
    console.log("Squirrel saved!");
    loadSquirrelsFromServer();
  });
}

function deleteSquirrelFromServer(squirrelId) {
  fetch("http://localhost:8080/squirrels/" + squirrelId, {
    method: "DELETE"
  }).then(function (response) {
    console.log("Squirrel deleted!");
    loadSquirrelsFromServer();
  });
}

loadSquirrelsFromServer();
