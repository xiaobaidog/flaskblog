

$(function () {

    $('#inputPhone').blur(function () {
        let phone = $(this).val();
        let span_ele = $(this).next('span');
        if (phone.length == 11) {
            span_ele.text('')
            $.get('/user/check_phone', {phone: phone}, function (data) {
                if (data.code != 200) {
                    span_ele.css({"color": "#ff0011", "font-size": "10px"})
                    span_ele.text(data.msg)
                }
            })
        } else {
            span_ele.css({"color": "#ff0011", "font-size": "10px"})
            span_ele.text('手机格式错误')
        }

    })

    $('.photo-del').click(function (){
        flag = confirm('是否删除该图片？')
        if(flag){
            let pid = $(this).attr('tag')
            location.href = '/user/delete_photo?pid='+pid
        }

    })
})