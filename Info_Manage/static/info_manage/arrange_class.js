$(document).ready(function () {
    $('#e_10 tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            $('#e_10').DataTable().$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );
    $('#delete_e_10').click( function () {
        teacher_id = $('#e_10').DataTable().row('.selected').data()[0];
        teacher_name = $('#e_10').DataTable().row('.selected').data()[1];
        $('#e_10').DataTable().row('.selected').remove().draw( false );
    } );
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
        if ( year == ''){
            alert('请选择排课学期!')
            return;
        }
        console.log(year);
        $('ul.setup-panel li:eq(1)').removeClass('disabled');
        $('ul.setup-panel li a[href="#step-2"]').trigger('click');
        $(this).remove();
        $.ajax({
            type: 'POST',
            url: '/arrange_step_1/',
            data: {"year": year},
            dataType: "json",
            success: function(result){
                if (result['result'] == 'success'){
                    location.reload();
                }
            },
            error: function (){

            }
        });
//        location.reload();


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

        if (leftTime == 0){
            window.location.reload();
        }
        if (isNaN(leftTime) || leftTime < 0){
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
        var status = 'start arrange';
        $.ajax({
            type: 'POST',
            url: '/arrange_step_3/',
            data: {"status": status},
            dataType: "json",
            success: function(result){
                console.log(result)
            },
            error: function (){

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
        var status = 'arrange over';
        $.ajax({
            type: 'POST',
            url: '/arrange_step_3/',
            data: {"status": status},
            dataType: "json",
            success: function(result){
                location.reload();
            },
            error: function (){

            }
        });


    });
    $('#activate-step-5').on('click', function(e) {

        var status = 'lock start';
        $.ajax({
            type: 'POST',
            url: '/arrange_step_5/',
            data: {"status": status},
            dataType: "json",
            success: function(result){
                if (result['status'] == 'Success'){
                    console.log(result)
                    $('ul.setup-panel li:eq(4)').removeClass('disabled');
                    $('ul.setup-panel li a[href="#step-5"]').trigger('click');
                    $(this).remove();
                }else{
                    alert(result['status'])
                }
            },
            error: function (){
                alert('No');
            }
        });
    });
    $("#arrange_class_with_teacher").on('click', function () {
        status='arrange main';
        alert(status);
        $.ajax({
            type: 'POST',
            url: '/arrange_step_3/',
            data: {"status": status},
            dataType: "json",
            success: function(result){

            },
            error: function (){
                alert('No');
            }
        });
    });
    $("#arrange_class_start").on('click', function () {
        var status = 'arrange main';
        $.ajax({
            type: 'POST',
            url: '/arrange_step_3/',
            data: {"status": status},
            dataType: "json",
            success: function(result){
                if (result['status'] == 'Pass'){
                    alert('排课成功')
                }
                else {
                    alert('排课异常')
                }
                document.getElementById('titleDuringArrange').setAttribute('hidden', 'hidden');
                document.getElementById('titleAfterArrange').removeAttribute('hidden');
                document.getElementById('export_course_report_1').removeAttribute('disabled');
                document.getElementById('analysis_course_report_1').removeAttribute('disabled');
            },
            error: function (){
//                alert('排课失败, 请检查教师申报信息');
            }
        });
    });
    $("#close_arrange_class2").on('click', function () {
        $('#arrangeClass2').modal('hide');
    });
    $("#search_teacher_id").click( function(){
        teacher_str = document.getElementById('e_10_teacher_str').value;
        console.log(teacher_str);
        $.ajax({
            type: 'POST',
            url: '/class_get_teacher_name/',
            data: {'teacher_str': teacher_str},
            dataType: "json",
            success: function(result){
                if (result['status'] == 'Success'){
                    document.getElementById('helpBlock1').innerHTML = result['teacher_id'];
                    document.getElementById('helpBlock2').innerHTML = result['teacher_name'];
                }else{
                    alert('没有找到该教师')
                }
            },
            error: function (){

            }
        });
    })
    $("#add_teacher_id").click( function(){
        teacher_id = document.getElementById('helpBlock1').innerText;
        teacher_name = document.getElementById('helpBlock2').innerText;
        if ( $.inArray(Number(teacher_id), $("#e_10").DataTable().column(0).data()) != -1){
            alert('该教师已经存在!');
            return
        }
        if ( teacher_id == '' || teacher_name == ''){
            alert('教师工号或教师姓名不能为空!')
            return
        }
        $("#e_10").DataTable().row.add([teacher_id, teacher_name]).draw();
        $('#add_teacher_e_10').modal('hide');
    })

    $('#lock_other_step').click( function(){
        var status = 'lock done';
        $.ajax({
            type: 'POST',
            url: '/arrange_step_5/',
            data: {"status": status},
            dataType: "json",
            success: function(result){
                if (result['status'] == 'Success'){
                    $('#confirmLockModal').modal('hide');
                    location.reload();
                }else{
                    alert(result['status'])
                }
            },
            error: function (){

            }
        });
    })
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

            },
            error: function (){

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
                    location.reload();
                }
            },
            error: function (){

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
            $('#setTimeout').modal('hide');
        },
        error: function (){

        }
    });
    location.reload();
}

function click_teacher(button_id){
    button_value = Number(document.getElementById(button_id).getAttribute('value'));
    if (button_value === 0){
        document.getElementById(button_id).text = '确认课程教师';
        document.getElementById(button_id).setAttribute('value', '1');
        $.ajax({
            type: 'POST',
            url: '/arrange_step_2/',
            data: {"id": button_id},
            dataType: "json",
            success: function(result){

            },
            error: function (){

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
                if (result['result'] === 'request end'){
                    document.getElementById('activate-step-3').removeAttribute('disabled');
                }
            },
            error: function (){

            }
        });
        button_value += 1;
    }else{
        button_value = 3;
    }
}

function arrange_start() {
    var status = 'init info';
    $.ajax({
        type: 'POST',
        url: '/arrange_step_3/',
        data: {"status": status},
        dataType: "json",
        success: function(result){
            page_info = result['result']['info'];
            console.log(page_info);
            initialize_arrange_class(page_info);
        },
        error: function (){

        }
    });
}

function initialize_arrange_class(page_info) {
    page_expect_1 = page_info[0];
    document.getElementById('lock_teacher_count').innerText = page_info[8];
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
    head = STUDENT_TYPE;
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
    var current_year = ''
    var post_url = '/history_export_teacher/?current_year='+current_year;
    location.replace(post_url);
}
function get_analysis_report_1(){
    var post_url = '/arrange_export_analysis_1/';
    location.replace(post_url);
}

function get_analysis_report_2(){
    var post_url = '/arrange_export_analysis_2/';
    location.replace(post_url);
}

function change_assign_teacher(){
    allow_teacher = document.getElementById('e_8').value;
    if ( $('#e_10').DataTable().rows().data().length != Number(allow_teacher) ){
        alert('替换教师数目不对!')
        return
    }
    notes = document.getElementById('e_11').value;
    if ( notes.length < 2){
        alert('请添加微调理由!')
        return
    }
    course_id = document.getElementById('e_0').value;
    str = "";
    for (var i = 0; i < $('#e_10').DataTable().rows().data().length; i++){
        if ( i == 0){
            str = $('#e_10').DataTable().rows().data()[i][1]
        }else{
            str = str + ',' +$('#e_10').DataTable().rows().data()[i][1]
        }
    }
    to_change_teacher = str
    $.ajax({
        type: 'POST',
        url: '/arrange_submit_adjust_request/',
        data: {"course_id": course_id, 'to_change_teacher': to_change_teacher, 'notes': notes},
        dataType: "json",
        success: function(result){
            if (result['status'] == 'success'){
                alert('微调申请提交成功，等待主管领导批准')
                $('#changeAssignTeacher').modal('hide');
            }
            else{
                alert(result['status'])
            }
        },
        error: function (){
            alert('修改失败');
        }
    });
}

function search_course_by_id(){
    course_id = document.getElementById('e_0').value;
    if ( course_id == ''){
        alert('请输入课程代码')
        return
    }
    $.ajax({
        type: 'POST',
        url: '/arrange_search_by_course_id/',
        data: {"course_id": course_id},
        dataType: "json",
        success: function(result){
            if (result['status'] == 'Success'){
                course_content = result['course'];
                for (var i=0; i < course_content.length; i++){
                    if ( i == 8  ||  i == 9 ){
                        continue;
                    }
                    document.getElementById('e_'+String(i+1)).value = course_content[i]
                }
                $('#e_9').DataTable({
                    dom: '<"top">rt<"bottom"><"clear">',
                    "searching": false,
                    "ordering": false,
                    "destroy": true,
                    "data": course_content[course_content.length-2],
                    "column":[
                        {title: '工号'},
                        {title: '姓名'}
                    ]
                });
                $('#e_10').DataTable({
                    dom: '<"top">rt<"bottom"><"clear">',
                    "searching": false,
                    "ordering": false,
                    "destroy": true,
                    "data": course_content[course_content.length-3],
                    "column":[
                        {title: '工号'},
                        {title: '姓名'}
                    ]
                });
            }
        },
        error: function (){
            alert('查找异常');
        }
    });
}

function disable_adjustment_button(type){
    type.setAttribute('disabled', 'disabled');
    button_id = type.id
    $.ajax({
        type: 'POST',
        url: '/arrange_change_button_status/',
        data: {"button_id": button_id},
        dataType: "json",
        success: function(result){
            if (result['status'] == 'Success'){

            }
        },
        error: function (){

        }
    });
}

function unlock_other_step(){
    var status = 'unlock';
    $.ajax({
        type: 'POST',
        url: '/arrange_step_5/',
        data: {"status": status},
        dataType: "json",
        success: function(result){
            if (result['status'] == 'Success'){
                alert('解锁成功!')
                location.reload();
            }else{
                alert(result['status'])
            }
        },
        error: function (){

        }
    });

}