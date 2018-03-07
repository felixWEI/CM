$(document).ready(function () {

    var navListItems = $('ul.setup-panel li a');
    var allWells = $('.setup-content');

    allWells.hide();

    navListItems.click(function(e)
    {
        e.preventDefault();
        var $target = $($(this).attr('href')),
            $item = $(this).closest('li');

        if (!$item.hasClass('disabled')) {
            navListItems.closest('li').removeClass('active');
            $item.addClass('active');
            allWells.hide();
            $target.show();
        }
    });

    $('ul.setup-panel li.active a').trigger('click');

    $('#activate-step-2').on('click', function() {
        var year = document.getElementById('step_1_select_list').value;
        console.log(year);
        $.ajax({
            type: 'POST',
            url: '/arrange_step_1/',
            data: {"year": year},
            dataType: "json",
            success: function(result){
                alert('Yes');
            },
            error: function (){
                alert('No');
            }
        });
        $('ul.setup-panel li:eq(1)').removeClass('disabled');
        $('ul.setup-panel li a[href="#step-2"]').trigger('click');
        $(this).remove();

    });
    // var t_s2_r1_c2 = 0;
    // var t_s2_r1_c3 = 0;
    // var t_s2_r1_c4 = 0;
    leftTimer();
    function leftTimer(){
        time_string = document.getElementById('s2_r2_c1').value;
        time_split = time_string.split(' ');
        year = time_split[0];
        month = time_split[1];
        day = time_split[2];
        hour = time_split[3];
        minute = time_split[4];
        second = 0;
        var leftTime = (new Date(year,month-1,day,hour,minute,second)) - (new Date()); //计算剩余的毫秒数
        if (isNaN(leftTime)){
            return;
        }
        var days = parseInt(leftTime / 1000 / 60 / 60 / 24 , 10); //计算剩余的天数
        var hours = parseInt(leftTime / 1000 / 60 / 60 % 24 , 10); //计算剩余的小时
        var minutes = parseInt(leftTime / 1000 / 60 % 60, 10);//计算剩余的分钟
        var seconds = parseInt(leftTime / 1000 % 60, 10);//计算剩余的秒数
        days = checkTime(days);
        hours = checkTime(hours);
        minutes = checkTime(minutes);
        seconds = checkTime(seconds);
        document.getElementById("timer").innerHTML = days+"天" + hours+"小时" + minutes+"分"+seconds+"秒";
        setInterval(function(){leftTimer()}, 1000);
    }
    function checkTime(i){ //将0-9的数字前面加上0，例1变为01
      if(i<10)
      {
        i = "0" + i;
      }
      return i;
    }

    $('#activate-step-3').on('click', function() {
        status = 'start arrange';
        $.ajax({
            type: 'POST',
            url: '/arrange_step_3/',
            data: {"status": status},
            dataType: "json",
            success: function(result){
                alert('Yes');
            },
            error: function (){
                alert('No');
            }
        });
        $('ul.setup-panel li:eq(2)').removeClass('disabled');
        $('ul.setup-panel li a[href="#step-3"]').trigger('click');
        $(this).remove();

    });

    $('#activate-step-4').on('click', function(e) {
        $('ul.setup-panel li:eq(3)').removeClass('disabled');
        $('ul.setup-panel li a[href="#step-4"]').trigger('click');
        $(this).remove();
        status = 'arrange over';
        $.ajax({
            type: 'POST',
            url: '/arrange_step_3/',
            data: {"status": status},
            dataType: "json",
            success: function(result){
                alert('Yes');
            },
            error: function (){
                alert('No');
            }
        });
    });
    $("#arrange_class_with_teacher").on('click', function () {
        status = 'arrange main';
        $.ajax({
            type: 'POST',
            url: '/arrange_step_3/',
            data: {"status": status},
            dataType: "json",
            success: function(result){
                alert('Yes');
            },
            error: function (){
                alert('No');
            }
        });
    });
    $("#arrange_class_start").on('click', function () {
        status = 'arrange main';
        $.ajax({
            type: 'POST',
            url: '/arrange_step_3/',
            data: {"status": status},
            dataType: "json",
            success: function(result){
                document.getElementById('titleDuringArrange').setAttribute('hidden', 'hidden');
                document.getElementById('titleAfterArrange').removeAttribute('hidden');
                document.getElementById('contentAfterArrange').removeAttribute('hidden');
            },
            error: function (){
                alert('No');
            }
        });
    });
    $("#close_arrange_class2").on('click', function () {
        $('#arrangeClass2').modal('hide');
    });
});
function click_class(button_id){
    button_value = Number(document.getElementById(button_id).getAttribute('value'));
    if (button_value === 0){
        document.getElementById(button_id).text = '确认课程信息';
        document.getElementById(button_id).setAttribute('value', '1');
        $.ajax({
            type: 'POST',
            url: '/arrange_step_2/',
            data: {"id": button_id},
            dataType: "json",
            success: function(result){
                alert('Yes');
            },
            error: function (){
                alert('No');
            }
        });
        button_value += 1;
    }else if(button_value === 1){
        document.getElementById(button_id).text = '课程已确认';
        document.getElementById(button_id).removeAttribute('href');
        document.getElementById(button_id).setAttribute('disabled', 'disabled');
        document.getElementById(button_id).setAttribute('value', '2');
        $.ajax({
            type: 'POST',
            url: '/arrange_step_2/',
            data: {"id": button_id},
            dataType: "json",
            success: function(result){
                if (result['result'] === 'start request'){
                    document.getElementById('s2_r2_c1').removeAttribute('disabled');
                }
            },
            error: function (){
                alert('No');
            }
        });
        button_value += 1;
    }else{
        button_value = 3;
    }
}

function start_request() {
    year = $('#setYear option:selected').val();
    month = $('#setMonth option:selected').val();
    day = $('#setDay option:selected').val();
    hour = $('#setHour option:selected').val();
    minute = $('#setMin option:selected').val();
    time = year+' '+month+' '+day+' '+hour+' '+minute;
    document.getElementById('s2_r2_c1').innerText = '距离申报课程截止时间还有';
    document.getElementById('s2_r2_c1').setAttribute('disabled', 'disabled');
    $.ajax({
        type: 'POST',
        url: '/arrange_step_2/',
        data: {"id": 's2_r2_c1', 'deadline':time},
        dataType: "json",
        success: function(result){
            alert('Yes')
        },
        error: function (){
            alert('No');
        }
        });
}

function click_teacher(button_id){
    button_value = Number(document.getElementById(button_id).getAttribute('value'));
    if (button_value === 0){
        document.getElementById(button_id).text = '确认教师';
        document.getElementById(button_id).setAttribute('value', '1');
        $.ajax({
            type: 'POST',
            url: '/arrange_step_2/',
            data: {"id": button_id},
            dataType: "json",
            success: function(result){
                alert('Yes');
            },
            error: function (){
                alert('No');
            }
        });
        button_value += 1;
    }else if(button_value === 1){
        document.getElementById(button_id).text = '教师已确认';
        document.getElementById(button_id).removeAttribute('href');
        document.getElementById(button_id).setAttribute('disabled', 'disabled');
        document.getElementById(button_id).setAttribute('value', '2');
        $.ajax({
            type: 'POST',
            url: '/arrange_step_2/',
            data: {"id": button_id},
            dataType: "json",
            success: function(result){
                alert('Yes')
            },
            error: function (){
                alert('No');
            }
        });
        button_value += 1;
    }else{
        button_value = 3;
    }
}

function arrange_start() {
    status = 'init info';
    $.ajax({
        type: 'POST',
        url: '/arrange_step_3/',
        data: {"status": status},
        dataType: "json",
        success: function(result){
            page_info = result['result']['info'];
            // console.log(page_info);
            initialize_arrange_class(page_info);
        },
        error: function (){
            alert('No');
        }
    });
}

function initialize_arrange_class(page_info) {
    document.getElementById('teacher_count').innerText = page_info[0];
    document.getElementById('teacher_with_expect').innerText = page_info[1];
    document.getElementById('total_hours_with_expect').innerText = page_info[2];
    document.getElementById('teacher_without_expect').innerText = page_info[3];
    document.getElementById('ave_hours_without_expect').innerText = page_info[4];
    course_degree_info = document.getElementById('course_degree_info');
    str = '<tr><td>人均课程数</td>';
    for(var index in page_info[5]){
        str += '<td>'+page_info[5][index]+'</td>';
    }
    str += '</tr>';
    course_degree_info.innerHTML = str;
    document.getElementById('total_courses').innerText = page_info[6];
    str2 = '';
    head = ['本科', '法学硕士', '法律硕士','博士'];
    for(var i in page_info[7]){
        str2 += '<tr><td>'+head[i]+'</td>';
        for(var j in page_info[7][i]){
            str2 += '<td>'+page_info[7][i][j]+'</td>';
        }
        str2 += '</tr>';
    }
    document.getElementById('whole_info_present').innerHTML = str2;
}
function get_course_report(){
    var post_url = '/arrange_export_report/';
    location.replace(post_url);
}