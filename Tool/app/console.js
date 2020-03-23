const user_name = "nomu"
$(document).on("keypress", ".console", function(e) {
    if (e.keyCode == 13) { // Enterが押された
        text_data = $('.console').val();
        var request = new XMLHttpRequest();
        URL = `https://j4179ibnf8.execute-api.us-east-2.amazonaws.com/develop/todocan/ls?user_name=${user_name}`;
        request.open('GET', URL, true);

        request.onload = function () {
            text_data += `\n${this.response}\n\nTODO>`;
            $('.console').val(text_data);
            var $scrollAuto = $('.console');
            $scrollAuto.animate({scrollTop: $scrollAuto[0].scrollHeight}, 'slow');
        }
        request.send();
    }
  });