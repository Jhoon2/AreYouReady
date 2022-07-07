let currentNum = 0;

$(document).ready(function () {
  listing();
});

function listing() {
  $.ajax({
    type: "GET",
    url: "/travel",
    data: {},
    success: function (response) {
      let rows = response["travels"];
      console.log(rows);
      for (let i = 0; i < rows.length; i++) {
        let comment = rows[i]["comment"];
        let title = rows[i]["title"];
        let desc = rows[i]["desc"];
        let image = rows[i]["image"];
        let num = rows[i]["num"];

        let temp_html = `
        <div class="card" onclick="modal_input_box(${num})" data-bs-toggle="modal" data-bs-target="#mymodal">
          <img src="${image}" class="card-img">
          <p class="card-text">${comment}</p>
          <div class="card-img-overlay" >
              <div class="card-info">
                <h5 class="card-title">${title}</h5>
                <p class="card-text">${desc}</p>
              </div>
          </div>
        </div>`;
        $("#cards-box").append(temp_html);
      }
    },
  });
}

function posting() {
  let url = $("#url").val();
  let comment = $("#comment").val();
  $.ajax({
    type: "POST",
    url: "/travel",
    data: { url_give: url, comment_give: comment },
    success: function (response) {
      alert(response["msg"]);
      window.location.reload();
    },
  });
}

function open_box() {
  $("#post-box").show();
}

function close_box() {
  $("#post-box").hide();
}

//
function show_supplies(num) {
  currentNum = num;
  $.ajax({
    type: "POST",
    url: "/travel/supplies",
    data: { num_give: num },
    success: function (response) {
      let rows = response["supplieslist"];
      $("#supplies-list").html("");
      let modal_title = response["modal-title"];
      console.log(modal_title)
      document.querySelector(".modal-title").innerText = modal_title + "에 가져가야할것들!";

      for (let i = 0; i < rows.length; i++) {
        let supplies = rows[i]["supplies"];
        let index = rows[i]["index"];
        let done = rows[i]["done"];
        console.log("index is ", index, supplies);
        let temp_html = ``;

        if (done == 0) {
          temp_html = `
<li>
<h2 class="supplies-text">✅ ${supplies}</h2>
<button onclick="done_supplies(${currentNum}, ${index}, event)" type="button" class="btn btn-outline-primary">완료!</button>
<button onclick="delete_supplies(${currentNum}, ${index}, event)" type="button" class="btn">삭제</button>
</li>
`;
        } else {
          temp_html = `
<li>
<h2 class="done">✔ ${supplies}</h2>
<button onclick="done_supplies(${currentNum}, ${index}, event)" type="button" class="btn btn-outline-success">해제!</button>
<button onclick="delete_supplies(${currentNum}, ${index}, event)" type="button" class="btn">삭제</button>
</li>
`;
        }
        $("#supplies-list").append(temp_html);
      }
    },
  });
}

function delete_supplies(currentNum, index, event) {
  let li = event.target.parentElement;

  $.ajax({
    type: "POST",
    url: "/supplies/delete",
    data: { currentNum_give: currentNum, index_give: index },
    success: function (response) {
      // alert(response['msg'])
      // window.location.reload();
      li.remove();
      modal_input_box(currentNum);
    },
  });
}

// function delete_all_supplies(currentNum) {


//   $.ajax({
//     type: "POST",
//     url: "/supplies/all_delete",
//     data: { currentNum_give: currentNum },
//     success: function (response) {
//       // alert(response['msg'])
//       // window.location.reload();
//     },
//   });
// } 

function save_supplies() {
  const input_tag = document.querySelector("#supplies-1");
  let supplies = $("#supplies-1").val();

  if (supplies !== "") {
    $.ajax({
      type: "POST",
      url: "/supplies",
      data: { supplies_give: supplies, num_give: currentNum },
      success: function (response) {
        let num = response["num"];
        let index = response["index"];
        console.log(num, index);

        // alert('준비물 등록 완료!')
        let li = document.createElement("li");
        let h2 = document.createElement("h2");
        let button = document.createElement("button");
        let button_1 = document.createElement("button");

        h2.classList.add("supplies-text");
        h2.innerText = `✅ ${supplies}`;

        button.innerText = "완료!";
        button.type = "button";
        button.classList.add("btn", "btn-outline-primary");
        button.setAttribute(
          "onclick",
          `done_supplies(${num}, ${index}, event)`
        );

        button_1.innerText = "삭제";
        button_1.type = "button";
        button_1.classList.add("btn");
        button_1.setAttribute(
          "onclick",
          `delete_supplies(${num}, ${index}, event)`
        );

        li.classList.add("list");
        li.appendChild(h2);
        li.appendChild(button);
        li.appendChild(button_1);

        document.querySelector("#supplies-list").appendChild(li);
        input_tag.value = null;
      },
    });
  } else {
    alert("입력하십시오!");
  }
}

function done_supplies(currentNum, index, e) {
  let li = e.target.parentElement;
  let h2 = li.children[0];
  let button = li.children[1];
  console.log(li);
  $.ajax({
    type: "POST",
    url: "/supplies/done",
    data: { currentNum_give: currentNum, index_give: index },
    success: function (response) {
      // alert(response["msg"])
      // window.location.reload()

      let done = response["supplieslist"][index - 1];
      console.log(done["done"]);
      if (done["done"] == 0) {
        h2.classList.add('done')
        h2.style = 'color:grey'
        h2.innerText = `✔ ${done['supplies']}`
        button.innerText = '해제!'
        button.classList.add('btn-outline-success')
      } else {
        h2.classList.remove('done')
        h2.style = 'color:black'
        h2.innerText = `✅ ${done['supplies']}`
        button.innerText = '완료!'
        button.classList.remove('btn-outline-success')
        button.classList.add('btn-outline-primary')
      }
    },
  });
}

function modal_input_box(num) {
  $("#suppliesInput").show();
  //num을 이용하여 show supplies 실행....
  console.log("ahahahahahah");
  show_supplies(num);
}

