$(document).ready(function () {
	t = $('#table_course_adjust').DataTable({
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

    $('#table_course_adjust tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            t.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );
    $('#e_11 tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            t.$('tr.selected').removeClass('selected');
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
                alert('Pass');
            },
            error: function(){
                alert('Delete fail');
            }
        })

    } );

    $('#delete_e_11').click( function () {
        teacher_id = $('#e_11').DataTable().row('.selected').data()[0];
        teacher_name = $('#e_11').DataTable().row('.selected').data()[1];
        $('#e_11').DataTable().row('.selected').remove().draw( false );
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
                    document.getElementById('page_expect_1').innerText = modify_0+"%";
                    document.getElementById('page_expect_2').innerText = modify_1+"%";
                    alert('修改期望成功')
                    location.reload();
                }else{
                    alert(result['status'])
                }
            },
            error: function (){
                alert('修改期望失败');
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
                    document.getElementById('a_1').value = result['raw_data'][0]
                    document.getElementById('a_2').value = result['raw_data'][1]
                    document.getElementById('a_3').value = result['raw_data'][2]
                    document.getElementById('a_4').value = result['raw_data'][3]
                    document.getElementById('a_5').value = result['raw_data'][4]
                    document.getElementById('a_6').value = result['raw_data'][5]
                    document.getElementById('a_7').value = result['raw_data'][6]
                    document.getElementById('a_8').value = result['raw_data'][7]
                    document.getElementById('a_9').value = result['raw_data'][8]
                    document.getElementById('a_10').value = result['raw_data'][9]
                    document.getElementById('a_1').setAttribute('disabled', 'disabled')
                    document.getElementById('a_5').setAttribute('disabled', 'disabled')
                    document.getElementById('a_6').setAttribute('disabled', 'disabled')
                    document.getElementById('a_7').setAttribute('disabled', 'disabled')
                    document.getElementById('a_8').setAttribute('disabled', 'disabled')
                    document.getElementById('a_9').setAttribute('disabled', 'disabled')
                    document.getElementById('a_10').setAttribute('disabled', 'disabled')
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
                    document.getElementById('a_1').removeAttribute('disabled')
                    document.getElementById('a_5').removeAttribute('disabled')
                    document.getElementById('a_6').removeAttribute('disabled')
                    document.getElementById('a_7').removeAttribute('disabled')
                    document.getElementById('a_8').removeAttribute('disabled')
                    document.getElementById('a_9').removeAttribute('disabled')
                    document.getElementById('a_10').removeAttribute('disabled')
                }
            },
            error: function (){
                alert('No');
            }
        });
    })
    $("#search_teacher_id").click( function(){
        teacher_str = document.getElementById('e_11_teacher_str').value;
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
        $("#e_11").DataTable().row.add([teacher_id, teacher_name]).draw();
        $('#add_teacher_e_11').modal('hide');
    })
//    initFileInput("excelFile","/class_table_upload/")
});
function cancel_request_show(){
    if ( t.row('.selected').length === 0 ){
        alert('没有选中的课程')
        return
    }
    $('#cancelRequestModal').modal('show');
    document.getElementById('cancel_CourseId').innerHTML = t.row('.selected').data()[0];
    document.getElementById('cancel_CourseName').innerHTML = t.row('.selected').data()[1];
    document.getElementById('cancel_TeacherBefore').innerHTML = t.row('.selected').data()[2];
    document.getElementById('cancel_TeacherAfter').innerHTML = t.row('.selected').data()[3];
    document.getElementById('cancel_notes').innerText = t.row('.selected').data()[5];
}
function cancel_request_submit(){
    $.ajax({
	    type: 'POST',
        url:'/teacher_reject_teacher_adjust/',
        data: {"course_id": t.row('.selected').data()[0]},
        dataType: "json",
        success: function (result) {
            alert(result['status']);
            $('#cancelRequestModal').modal('hide')
        },
        error: function () {
            alert('驳回异常');
        }

	})
}
function approve_request_show(){
    if ( t.row('.selected').length === 0 ){
        alert('没有选中的课程')
        return
    }
    $('#approveRequestModal').modal('show');
    document.getElementById('approve_CourseId').innerHTML = t.row('.selected').data()[0];
    document.getElementById('approve_CourseName').innerHTML = t.row('.selected').data()[1];
    document.getElementById('approve_TeacherBefore').innerHTML = t.row('.selected').data()[2];
    document.getElementById('approve_TeacherAfter').innerHTML = t.row('.selected').data()[3];
    document.getElementById('approve_notes').innerText = t.row('.selected').data()[5];
}
function approve_request_submit(){
    $.ajax({
	    type: 'POST',
        url:'/teacher_approve_teacher_adjust/',
        data: {"course_id": t.row('.selected').data()[0]},
        dataType: "json",
        success: function (result) {
            alert(result['status']);
            $('#approveRequestModal').modal('hide')
            location.reload();
        },
        error: function () {
            alert('驳回异常');
        }

	})
}
