$('.toggle1').on('click', function() {
    $('.toggle1').hide();
    $('.toggle2').show();
    $('.toggle2').css("display", "inline-block");
    $('.icon').show();
    $('.console').show();
    $('.icon').css("display", "inline-block");
    $('.console').css("display", "inline-block");
  });

$('.toggle2').on('click', function() {
    $('.toggle2').hide();
    $('.toggle1').show();
    $('.toggle1').css("display", "inline-block");
    $('.icon').hide();
    $('.console').hide();
  });
  