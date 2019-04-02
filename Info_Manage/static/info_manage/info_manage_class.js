$(document).ready(function () {
	t = $('#table_course_manage').DataTable({
        dom: 'Blfrtip',
        lengthMenu: [50,100],
        buttons: [ {
            extend: 'excelHtml5',
            customize: function( xlsx ) {
                var sheet = xlsx.xl.worksheets['sheet1.xml'];
                $('row c[r^="C"]', sheet).attr( 's', '2' );
            }
        } ]
	});


    $('#table_course_manage tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            t.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );
    $('#e_13 tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            $('#e_13').DataTable().$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );

    $('#delete').click( function () {
        course_id = t.row('.selected').data()[0];
        console.log(course_id)
        student_type = t.row('.selected').data()[2]
        class_grade = t.row('.selected').data()[3]
        class_name = t.row('.selected').data()[4]
        combine_data = student_type+'-'+class_grade+'_'+class_name
        t.row('.selected').remove().draw( false );
        $.ajax({
            type: 'POST',
            url: '/class_delete_one_row/',
            data: {'course_id': course_id, 'old_data':combine_data},
            dataType: 'json',
            success: function(result){
                alert('删除成功!')
                $('#confirmDeleteModal').modal('hide');
                location.reload();
            },
            error: function(){
                alert('Delete fail');
            }
        })

    } );

    $('#delete_e_13').click( function () {
        teacher_id = $('#e_13').DataTable().row('.selected').data()[0];
        teacher_name = $('#e_13').DataTable().row('.selected').data()[1];
        $('#e_13').DataTable().row('.selected').remove().draw( false );
    } );

    $('#edit_teacher_info').click( function(){
        teacher_code = document.getElementById('teacher_code_2').value
        teacher_name = document.getElementById('teacher_name_2').value
        time_first_season = document.getElementById('time_first_season_2').value
        time_second_season = document.getElementById('time_second_season_2').value
        class_order = document.getElementById('class_order_2').value
        t.row('.selected').data([teacher_code, teacher_name, time_first_season, time_second_season, class_order]).draw();
    });

	$('#check_table').click( function(){

	    var table_info = t.rows().data();
	    var table_str = JSON.stringify(table_info);
	    $.ajax({
            type: 'POST',
            url: '/teacher_save_and_config/',
            data: {"teacher_table": table_str},
            dataType: "json",
            success: function(result){
                alert('Yes');
            },
            error: function (){
                alert('No');
            }

	    })

	});
    $("#submit_semester_expect").click( function () {
        modify_0 = document.getElementById('modify_0').value;
        modify_1 = document.getElementById('modify_1').value;
        $.ajax({
            type: 'POST',
            url: '/teacher_change_expect/',
            data: {"modify_0": modify_0, 'modify_1':modify_1},
            dataType: "json",
            success: function(result){
                if (result['status']=='Success'){
                    alert('修改期望成功')
                }else{
                    alert(result['status'])
                }
            },
            error: function (){
                alert('No');
            }
        });
    });
    $("#a_search_course_id").click( function(){
        course_id = document.getElementById('a_0').value
        $.ajax({
            type: 'POST',
            url: '/class_search_from_course_id/',
            data: {'course_id': course_id},
            dataType: "json",
            success: function(result){
                if (result['status'] == 'Success'){
                    console.log(result['raw_data'][5])
                    document.getElementById('a_1').value = result['raw_data'][0]
                    document.getElementById('a_2').value = result['raw_data'][1]
                    document.getElementById('a_3').value = result['raw_data'][2]
                    document.getElementById('a_4').value = result['raw_data'][3]
                    document.getElementById('a_5').value = result['raw_data'][4]
                    document.getElementById('a_6').value = result['raw_data'][5]
                    document.getElementById('a_7').value = Number(result['raw_data'][6])
                    document.getElementById('a_8').value = result['raw_data'][7]
                    document.getElementById('a_9').value = result['raw_data'][8]
                    document.getElementById('a_10').value = result['raw_data'][9]
                    document.getElementById('a_11').value = result['raw_data'][10]
                    document.getElementById('a_12').value = result['raw_data'][11]
                    document.getElementById('a_1').setAttribute('disabled', 'disabled')
                    document.getElementById('a_2').removeAttribute('disabled')
                    document.getElementById('a_3').removeAttribute('disabled')
                    document.getElementById('a_4').removeAttribute('disabled')
                    document.getElementById('a_5').removeAttribute('disabled')
                    document.getElementById('a_6').setAttribute('disabled', 'disabled')
                    document.getElementById('a_7').setAttribute('disabled', 'disabled')
                    document.getElementById('a_8').setAttribute('disabled', 'disabled')
                    document.getElementById('a_9').setAttribute('disabled', 'disabled')
                    document.getElementById('a_10').removeAttribute('disabled')
                    document.getElementById('a_11').setAttribute('disabled', 'disabled')
                    document.getElementById('a_12').setAttribute('disabled', 'disabled')
                    document.getElementById('a_14').removeAttribute('disabled')
                    document.getElementById('a_15').removeAttribute('disabled')
                }else{
                    document.getElementById('a_1').value = ''
                    document.getElementById('a_2').value = ''
                    document.getElementById('a_3').value = ''
                    document.getElementById('a_4').value = ''
                    document.getElementById('a_5').value = ''
                    document.getElementById('a_6').value = ''
                    document.getElementById('a_7').value = ''
                    document.getElementById('a_8').value = ''
                    document.getElementById('a_9').value = ''
                    document.getElementById('a_10').value = ''
                    document.getElementById('a_12').value = ''
                    document.getElementById('a_1').removeAttribute('disabled')
                    document.getElementById('a_2').removeAttribute('disabled')
                    document.getElementById('a_3').removeAttribute('disabled')
                    document.getElementById('a_4').removeAttribute('disabled')
                    document.getElementById('a_5').removeAttribute('disabled')
                    document.getElementById('a_6').removeAttribute('disabled')
                    document.getElementById('a_7').removeAttribute('disabled')
                    document.getElementById('a_8').removeAttribute('disabled')
                    document.getElementById('a_9').removeAttribute('disabled')
                    document.getElementById('a_10').removeAttribute('disabled')
                    document.getElementById('a_11').removeAttribute('disabled')
                    document.getElementById('a_12').removeAttribute('disabled')
                    document.getElementById('a_14').removeAttribute('disabled')
                    document.getElementById('a_15').removeAttribute('disabled')
                }
            },
            error: function (){
                alert('No');
            }
        });
    })
    $("#search_teacher_id").click( function(){
        teacher_str = document.getElementById('e_13_teacher_str').value;
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
                alert('No');
            }
        });
    })
    $("#add_teacher_id").click( function(){
        teacher_id = document.getElementById('helpBlock1').innerText;
        teacher_name = document.getElementById('helpBlock2').innerText;
        if ( $.inArray((teacher_id), $("#e_13").DataTable().column(0).data()) != -1){
            alert('该教师已经存在!');
            return
        }
        if ( teacher_id == '' || teacher_name == ''){
            alert('教师工号或教师姓名不能为空!')
            return
        }
        $("#e_13").DataTable().row.add([teacher_id, teacher_name]).draw();
        $('#add_teacher_e_13').modal('hide');
    })
    initFileInput("excelFile","/class_table_upload/")
});
function submit_checkbox_info(){
    str1 = "";
    if (document.getElementById('c_student_type_1').checked == true){
        str1 += "本科 ";
    }
    if (document.getElementById('c_student_type_2').checked == true){
        str1 += "法学硕士 ";
    }
    if (document.getElementById('c_student_type_3').checked == true){
        str1 += "法律硕士 ";
    }
    if (document.getElementById('c_student_type_4').checked == true){
        str1 += "法学博士 ";
    }
    str2 = "";
    if (document.getElementById('c_semester_1').checked == true){
        str2 += "一 ";
    }
    if (document.getElementById('c_semester_2').checked == true){
        str2 += "二 ";
    }
    var major_list = Array();
    $("input[name='major_check_list']:checked").each(function(i){
        major_list[i] = $(this).val();
    });
    major_list = JSON.stringify(major_list);
    console.log(major_list);
    $.ajax({
        type: 'POST',
        url: '/class_filter_by_submit/',
        data: {'type': str1, 'semester':str2, 'table_id':'table_course_manage','major_list': major_list},
        dataType: "json",
        success: function(result){
            console.log(result['result'])
            $('#table_course_manage').DataTable().clear();
            for (var i = 0; i < result['result'].length; i++){
                $('#table_course_manage').DataTable().row.add(result['result'][i])
            }
            $('#table_course_manage').DataTable().draw();
        },
        error: function (){
            alert('No');
        }
    });
}
function add_course_info(length){
    row_data = Array();
    for (var i=0; i < Number(length); i++ ){
        if ( document.getElementById('a_'+String(i)).value !== undefined ){
            row_data[i] = document.getElementById('a_'+String(i)).value;
            if (i==0){
                row_data[i] = row_data[i].toUpperCase();
            }
        }else{
            row_data[i] = "";
        }
//        console.log(document.getElementById(i).value);
    }
    t.row.add(row_data).draw();
    var old_data = ''
    var row_str = JSON.stringify(row_data);
    $.ajax({
        type: 'POST',
            url:'/class_save_one_row/',
            data: {"row_data": row_str, 'old_data':old_data},
            dataType: "json",
            success: function (result) {
                alert('添加成功');
                location.reload();
            },
            error: function () {
                alert('fail');
            }

    })
}
function edit_course_info(){
    if ( t.row('.selected').length === 0 ){
        alert('没有选中的课程')
        return
    }
    $('#editModal').modal('show');
    document.getElementById('e_0').value = t.row('.selected').data()[0];
    document.getElementById('e_1').value = t.row('.selected').data()[1];
    document.getElementById('e_3').options.length = 0
    document.getElementById('e_4').options.length = 0
    document.getElementById('e_5').options.length = 0
    document.getElementById('e_6').options.length = 0
    document.getElementById('e_7').options.length = 0
    document.getElementById('e_8').options.length = 0
//    for (var i in STUDENT_TYPE){
//        document.getElementById('e_3').options.add(new Option(STUDENT_TYPE[i]))
//    }
    for (var i in STUDENT_TYPE){
        document.getElementById('e_3').options.add(new Option(STUDENT_TYPE[i]))
    }
    for (var i=0; i < 4; i++){
        year = Number(current_year) - i
        document.getElementById('e_4').options.add(new Option(year))
    }
    for (var i in CLASS_NAME_LIST){
        document.getElementById('e_5').options.add(new Option(CLASS_NAME_LIST[i]))
    }
    for (var i in SEMESTER){
        document.getElementById('e_6').options.add(new Option(SEMESTER[i]))
    }
    for (var i in COURSE_HOUR){
        document.getElementById('e_7').options.add(new Option(COURSE_HOUR[i]))
    }
    for (var i in COURSE_DEGREE){
        document.getElementById('e_8').options.add(new Option(COURSE_DEGREE[i]))
    }
    for (var i in COURSE_TYPE){
        document.getElementById('e_9').options.add(new Option(COURSE_TYPE[i]))
    }

    document.getElementById('e_2').innerHTML = '<option>'+t.row('.selected').data()[2]+'</option>'+document.getElementById('e_2').innerHTML;
    document.getElementById('e_3').innerHTML = '<option>'+t.row('.selected').data()[3]+'</option>'+document.getElementById('e_3').innerHTML;
    document.getElementById('e_4').innerHTML = '<option>'+t.row('.selected').data()[4]+'</option>'+document.getElementById('e_4').innerHTML;
    document.getElementById('e_5').innerHTML = '<option>'+t.row('.selected').data()[5]+'</option>'+document.getElementById('e_5').innerHTML;
    document.getElementById('e_6').innerHTML = '<option>'+t.row('.selected').data()[6]+'</option>'+document.getElementById('e_6').innerHTML;
    document.getElementById('e_7').innerHTML = '<option>'+t.row('.selected').data()[7]+'</option>'+document.getElementById('e_7').innerHTML;
    document.getElementById('e_8').innerHTML = '<option>'+t.row('.selected').data()[8]+'</option>'+document.getElementById('e_8').innerHTML;
    document.getElementById('e_9').value = t.row('.selected').data()[9];
    document.getElementById('e_10').innerHTML = '<option>'+t.row('.selected').data()[10]+'</option>'+document.getElementById('e_10').innerHTML;
    document.getElementById('e_11').value = t.row('.selected').data()[11];
    document.getElementById('e_12').value = t.row('.selected').data()[12];
    document.getElementById('e_14').value = t.row('.selected').data()[14];
    document.getElementById('e_15').value = t.row('.selected').data()[15];
	$.ajax({
	    type: 'POST',
        url:'/class_get_suit_teacher/',
        data: {"course_id": t.row('.selected').data()[0]},
        dataType: "json",
        success: function (result) {
            var teacher_list = result['result_list'];
//            $('#e_11').DataTable().clear();
            $('#e_13').DataTable({
                dom: '<"top">rt<"bottom"><"clear">',
                "searching": false,
                "ordering": false,
                "destroy": true,
                "data": teacher_list,
                "column":[
                    {title: '工号'},
                    {title: '姓名'}
                ]
            });
        },
        error: function () {
            alert('fail');
        }

	})

}
function request_course(){
    if ( t.row('.selected').length === 0 ){
        alert('没有选中的课程')
        return
    }
    $('#requestModal').modal('show');
    document.getElementById('e_0').value = t.row('.selected').data()[0];
    document.getElementById('e_1').value = t.row('.selected').data()[1];
    document.getElementById('e_2').innerHTML = '<option>'+t.row('.selected').data()[2]+'</option>'+document.getElementById('e_2').innerHTML;
    document.getElementById('e_4').value = t.row('.selected').data()[3];
    document.getElementById('e_5').innerHTML = '<option>'+t.row('.selected').data()[4]+'</option>'+document.getElementById('e_5').innerHTML;
    document.getElementById('e_6').innerHTML = '<option>'+t.row('.selected').data()[5]+'</option>'+document.getElementById('e_6').innerHTML;
    document.getElementById('e_7').innerHTML = '<option>'+t.row('.selected').data()[6]+'</option>'+document.getElementById('e_7').innerHTML;
    document.getElementById('e_8').value = t.row('.selected').data()[7];
    document.getElementById('e_9').value = t.row('.selected').data()[8];
    document.getElementById('e_10').value = t.row('.selected').data()[9];
}
function cancel_request(){
    if ( t.row('.selected').length === 0 ){
        alert('没有选中的课程')
        return
    }
    $('#cancelModal').modal('show');
    console.log(t.row('.selected').data());
    document.getElementById('c_0').value = t.row('.selected').data()[0];
    document.getElementById('c_1').value = t.row('.selected').data()[1];
    document.getElementById('c_2').innerHTML = '<option>'+t.row('.selected').data()[2]+'</option>'+document.getElementById('e_2').innerHTML;
    document.getElementById('c_4').value = t.row('.selected').data()[3];
    document.getElementById('c_5').innerHTML = '<option>'+t.row('.selected').data()[4]+'</option>'+document.getElementById('e_5').innerHTML;
    document.getElementById('c_6').innerHTML = '<option>'+t.row('.selected').data()[5]+'</option>'+document.getElementById('e_6').innerHTML;
    document.getElementById('c_7').innerHTML = '<option>'+t.row('.selected').data()[6]+'</option>'+document.getElementById('e_7').innerHTML;
    document.getElementById('c_8').value = t.row('.selected').data()[7];
    document.getElementById('c_9').value = t.row('.selected').data()[8];
    document.getElementById('c_10').value = t.row('.selected').data()[9];
}

function submit_edit_info(){
    row_data = Array();
    for (var i=0; i < 16; i++ ){
        if ( document.getElementById('e_'+String(i)).value !== undefined ){
            row_data[i] = document.getElementById('e_'+String(i)).value;
            if (i==0){
                row_data[i] = row_data[i].toUpperCase();
            }
        }else{
            row_data[i] = "";
        }
//        console.log(document.getElementById(i).value);
    }
    str = "";
    for (var j=0; j < $("#e_13").DataTable().rows().data().length; j++){
        str += $("#e_13").DataTable().rows(j).data()[0][1];
        if( j <  $("#e_13").DataTable().rows().data().length-1){
            str += ',';
        }
    }
    course_id = t.row('.selected').data()[0]
    major =  t.row('.selected').data()[2]
    student_type = t.row('.selected').data()[3]
    class_grade = t.row('.selected').data()[4]
    class_name = t.row('.selected').data()[5]
    combine_data = student_type+'-'+class_grade+'_'+class_name
    console.log(combine_data)
    row_data[13] = str;
    t.row('.selected').data(row_data).draw();
    console.log(row_data);
    var row_str = JSON.stringify(row_data);
    $.ajax({
        type: 'POST',
        url:'/class_save_one_row/',
        data: {"row_data": row_str, 'old_data':combine_data, 'old_course_id':course_id},
        dataType: "json",
        success: function (result) {
            alert('编辑成功');
            location.reload()
        },
        error: function () {
            alert('fail');
        }

    })

}
function submit_request(){
    course_id = document.getElementById('e_0').value;
    $.ajax({
        type: 'POST',
        url:'/teacher_request_course/',
        data: {"course_id": course_id},
        dataType: "json",
        success: function (result) {
            if (result['status'] == 'Success'){
                alert('申报成功')
            }else{
                alert(result['status'])
            }
            $('#requestModal').modal('hide')
        },
        error: function () {
            alert('fail');
        }

    })
}
function submit_cancel(){
    course_id = document.getElementById('c_0').value;
    var status = 'cancel'
    $.ajax({
        type: 'POST',
        url:'/teacher_request_course/',
        data: {"course_id": course_id, 'status':status},
        dataType: "json",
        success: function (result) {
            if (result['status'] == 'Success'){
                alert('取消申报成功')
            }else{
                alert(result['status'])
            }
            $('#cancelModal').modal('hide')
        },
        error: function () {
            alert('fail');
        }

    })
}
function initFileInput(ctrlName, uploadUrl) {
    var control = $('#' + ctrlName);
    control.fileinput({
        language: 'zh', //设置语言
        uploadUrl: uploadUrl, //上传的地址
        uploadAsync: true, //默认异步上传
        showCaption: true,//是否显示标题
        showUpload: true, //是否显示上传按钮
        browseClass: "btn btn-primary", //按钮样式
        allowedFileExtensions: ["xls", "xlsx", 'txt'], //接收的文件后缀
        maxFileCount: 1,//最大上传文件数限制
        previewFileIcon: '<i class="glyphicon glyphicon-file"></i>',
        showPreview: true, //是否显示预览
        previewFileIconSettings: {
            'docx': '<i ass="fa fa-file-word-o text-primary"></i>',
            'xlsx': '<i class="fa fa-file-excel-o text-success"></i>',
            'xls': '<i class="fa fa-file-excel-o text-success"></i>',
            'pptx': '<i class="fa fa-file-powerpoint-o text-danger"></i>',
            'jpg': '<i class="fa fa-file-photo-o text-warning"></i>',
            'pdf': '<i class="fa fa-file-archive-o text-muted"></i>',
            'zip': '<i class="fa fa-file-archive-o text-muted"></i>',
        },
        uploadExtraData: function () {
            var extraValue = "test";
            return {"excelType": extraValue};
        }
    });
}

function confirm_delete_class(){
    if ( t.row('.selected').length === 0 ){
        alert('没有选中的课程')
        return
    }
    $('#confirmDeleteModal').modal('show');
    document.getElementById('p_danger_1').innerText = t.row('.selected').data()
}

$("#excelFile").on("fileuploaded", function (event, data, previewId, index) {
    console.log(data);
    if(data.response.result == 'Pass')
    {
        alert(data.files[index].name + "上传成功!");
    //关闭
        $(".close").click();
        location.reload();
    }
    else{
        alert(data.files[index].name + "上传失败!" + data.response.message);
    //重置
    $("#excelFile").fileinput("clear");
    $("#excelFile").fileinput("reset");
    $('#excelFile').fileinput('refresh');
    $('#excelFile').fileinput('enable');
    }
})