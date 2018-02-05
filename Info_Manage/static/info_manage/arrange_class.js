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

    })
    var t_s2_r1_c2 = 0;
    var t_s2_r1_c3 = 0;
    var t_s2_r1_c4 = 0;
//    $('#s2_r1_c1').on('click', function(){
//        t_s2_r1_c1 = Number(document.getElementById('s2_r1_c1').getAttribute('value'));
//        if (t_s2_r1_c1 === 0){
//            document.getElementById('s2_r1_c1').text = '确认课程信息';
//            document.getElementById('s2_r1_c1').setAttribute('value', '1');
//            $.ajax({
//                type: 'POST',
//                url: '/arrange_step_2/',
//                data: {"id": 's2_r1_c1'},
//                dataType: "json",
//                success: function(result){
//                    alert('Yes');
//                },
//                error: function (){
//                    alert('No');
//                }
//            });
//            t_s2_r1_c1 += 1;
//        }else if(t_s2_r1_c1 === 1){
//            document.getElementById('s2_r1_c1').text = '课程已确认';
//            document.getElementById('s2_r1_c1').removeAttribute('href');
//            document.getElementById('s2_r1_c1').setAttribute('disabled', 'disabled');
//            document.getElementById('s2_r1_c1').setAttribute('value', '2');
//            $.ajax({
//                type: 'POST',
//                url: '/arrange_step_2/',
//                data: {"id": 's2_r1_c1'},
//                dataType: "json",
//                success: function(result){
//                    alert('Yes');
//                },
//                error: function (){
//                    alert('No');
//                }
//            });
//            t_s2_r1_c1 += 1;
//        }else{
//            t_s2_r1_c1 = 3;
//        }
//    })
//    $('#s2_r1_c2').on('click', function(){
//        if (t_s2_r1_c2 === 0){
//            document.getElementById('s2_r1_c2').text = '确认课程信息';
//            t_s2_r1_c2 += 1;
//        }else if(t_s2_r1_c2 === 1){
//            document.getElementById('s2_r1_c2').text = '课程已确认';
//            document.getElementById('s2_r1_c2').removeAttribute('href');
//            document.getElementById('s2_r1_c2').setAttribute('disabled', 'disabled');
//            t_s2_r1_c2 += 1;
//        }else{
//            t_s2_r1_c2 = 3;
//        }
//    })
//    $('#s2_r1_c3').on('click', function(){
//        if (t_s2_r1_c3 === 0){
//            document.getElementById('s2_r1_c3').text = '确认课程信息';
//            t_s2_r1_c3 += 1;
//        }else if(t_s2_r1_c3 === 1){
//            document.getElementById('s2_r1_c3').text = '课程已确认';
//            document.getElementById('s2_r1_c3').removeAttribute('href');
//            document.getElementById('s2_r1_c3').setAttribute('disabled', 'disabled');
//            t_s2_r1_c3 += 1;
//        }else{
//            t_s2_r1_c3 = 3;
//        }
//    })
//    $('#s2_r1_c4').on('click', function(){
//        if (t_s2_r1_c4 === 0){
//            document.getElementById('s2_r1_c4').text = '确认课程信息';
//            t_s2_r1_c4 += 1;
//        }else if(t_s2_r1_c4 === 1){
//            document.getElementById('s2_r1_c4').text = '课程已确认';
//            document.getElementById('s2_r1_c4').removeAttribute('href');
//            document.getElementById('s2_r1_c4').setAttribute('disabled', 'disabled');
//            t_s2_r1_c4 += 1;
//        }else{
//            t_s2_r1_c4 = 3;
//        }
//    })

    $('#activate-step-3').on('click', function(e) {
        $('ul.setup-panel li:eq(2)').removeClass('disabled');
        $('ul.setup-panel li a[href="#step-3"]').trigger('click');
        $(this).remove();
    })

    $('#activate-step-4').on('click', function(e) {
        $('ul.setup-panel li:eq(3)').removeClass('disabled');
        $('ul.setup-panel li a[href="#step-4"]').trigger('click');
        $(this).remove();
    })

    $('#activate-step-3').on('click', function(e) {
        $('ul.setup-panel li:eq(2)').removeClass('disabled');
        $('ul.setup-panel li a[href="#step-3"]').trigger('click');
        $(this).remove();
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
                alert('Yes');
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