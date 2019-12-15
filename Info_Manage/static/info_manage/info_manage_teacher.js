$(document).ready(function () {
	t = $('#table_teacher').DataTable({
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

    $('#table_teacher tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            t.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );

    $('#table_course tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            t.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );

    $('#delete').click( function () {
        t.row('.selected').remove().draw( false );
    } );

	$('#edit_table').click( function(){
        if ( t.row('.selected').length === 0 ){
            alert('没有选择的教师')
            return
        }
        $('#editModal').modal('show')
        for (var i=0; i < t.row('.selected').data().length; i++){
            document.getElementById(i.toString()).value = t.row('.selected').data()[i];
        }
	});
	$('#approve_table').click( function(){
        if ( t.row('.selected').length === 0 ){
            alert('没有选择的教师')
            return
        }
        $('#approveModal').modal('show')
        for (var i=0; i < t.row('.selected').data().length; i++){
            id = 'a_'+i.toString()
            document.getElementById(id).value = t.row('.selected').data()[i];
        }
	});

    $('#edit_teacher_info').click( function(){
        teacher_code = document.getElementById('0').value
        teacher_name = document.getElementById('1').value
        major = document.getElementById('2').value
        teacher_type = document.getElementById('3').value
        teacher_title = document.getElementById('4').value
        birthday = document.getElementById('5').value
        first_semester_expect = document.getElementById('6').value
        second_semester_expect = document.getElementById('7').value
        hours_semester_1 = document.getElementById('8').value
        hours_semester_2 = document.getElementById('9').value
        degree_semester_1 = document.getElementById('10').value
        degree_semester_2 = document.getElementById('11').value
        teacher_apply_status = document.getElementById('12').value
        notes = document.getElementById('13').value
        apply_course_count = document.getElementById('14').value
        lock_state = document.getElementById('15').value
        t.row('.selected').data([teacher_code, teacher_name, major, teacher_type, teacher_title, birthday,
        first_semester_expect, second_semester_expect, hours_semester_1,hours_semester_2,
        degree_semester_1, degree_semester_2, teacher_apply_status, notes, apply_course_count, lock_state]).draw();
        $.ajax({
            type: 'POST',
            url: '/teacher_change_expect/',
            data: {"modify_0": first_semester_expect, 'modify_1':second_semester_expect, 'teacher_id':teacher_code, 'lock_state':lock_state},
            dataType: "json",
            success: function(result){
                if (result['status']=='Success'){
                    alert('修改期望成功')
                    location.reload();
                }else{
                    alert(result['status'])
                }
            },
            error: function (){
                console.log('No');
            }
        });
    });
    $('#approve_teacher_request').click( function(){
        teacher_code = document.getElementById('a_0').value
        teacher_name = document.getElementById('a_1').value
        major = document.getElementById('a_2').value
        teacher_type = document.getElementById('a_3').value
        teacher_title = document.getElementById('a_4').value
        birthday = document.getElementById('a_5').value
        first_semester_expect = document.getElementById('a_6').value
        second_semester_expect = document.getElementById('a_7').value
        hours_semester_1 = document.getElementById('a_8').value
        hours_semester_2 = document.getElementById('a_9').value
        degree_semester_1 = document.getElementById('a_10').value
        degree_semester_2 = document.getElementById('a_11').value
        teacher_apply_status = document.getElementById('a_12').value
        notes = document.getElementById('a_13').value
        apply_course_count = document.getElementById('a_14').value
        lock_state = document.getElementById('a_15').value
        t.row('.selected').data([teacher_code, teacher_name, major, teacher_type, teacher_title, birthday,
        first_semester_expect, second_semester_expect, hours_semester_1,hours_semester_2,
        degree_semester_1, degree_semester_2, teacher_apply_status, notes, apply_course_count, lock_state]).draw();
        var status = 'approve'
        $.ajax({
            type: 'POST',
            url: '/teacher_submit_apply_status/',
            data: {'teacher_id':teacher_code, 'status':status},
            dataType: "json",
            success: function(result){
                if (result['status']=='Success'){
                    alert('通过撤销申请')
                    location.reload();
                }else{
                    alert(result['status'])
                }
            },
            error: function (){
                console.log('No');
            }
        });
    });

	$('#add_teacher_info').on('click',function(){
        if (document.getElementById('teacher_code').value in t.column(0).data()){
            alert('Teacher Id already exist!!');
            return
        }
	    t.row.add([
            document.getElementById('teacher_code').value,
            document.getElementById('teacher_name').value,
            document.getElementById('time_first_season').value,
            document.getElementById('time_second_season').value,
            document.getElementById('class_order').value,
	    ]).draw();
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

//	$('#submit_file').click( function() {
//	    file = document.getElementById('InputFile').value;
//	    initFileInput('InputFile', file)
//	    console.log(file);
//	})
    initFileInput("excelFile","/teacher_table_upload/")
    initFileInput("excelFile2","/teacher_help_declare_upload/")
});

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
});
$("#excelFile2").on("fileuploaded", function (event, data, previewId, index) {
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
    $("#excelFile2").fileinput("clear");
    $("#excelFile2").fileinput("reset");
    $('#excelFile2').fileinput('refresh');
    $('#excelFile2').fileinput('enable');
    }
});