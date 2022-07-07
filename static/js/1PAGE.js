$(document).ready(function () {

  $.ajax({
      type: "GET",
      url: "http://spartacodingclub.shop/sparta_api/weather/seoul",
      data: {},
      success: function (response) {
          let temp = response['temp']
          $('#temp').text(temp)
      }
  })

});





let nums = 0;
$('.menu-trigger').on('click', function () {
  // console.log('d')
  if (nums % 2 === 0) {
      document.querySelector('.list-group').classList.add('show')
      nums++;
  } else {
      document.querySelector('.list-group').classList.remove('show')
      nums++;
  }

})

var burger = $('.menu-trigger');

burger.each(function (index) {
  var $this = $(this);

  $this.on('click', function (e) {
      e.preventDefault();
      $(this).toggleClass('active-' + (index + 1));
  })
});