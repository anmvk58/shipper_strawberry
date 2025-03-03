// init count variable
var count = 0
var total_bill = 0
var list_bill = []

// function to check bill_code validate first
function check_bill_code(bill_code) {
    if (bill_code === '') {
        pushNotification('Bill Code Error', 'Mã bill trống !!!', 'error')
        return false
    }

    if (!list_bill.includes(bill_code)) {
        list_bill.push(bill_code)
        return true
    } else {
        pushNotification('Bill Code Exsist', 'Mã bill đã tồn tại !!!', 'error')
        $('#bill_input').val('');
        return false
    }

}


// function to check bill_code correct first
function reset_bill() {
    $("#datatables-basic tbody").empty()
    count = 0
    total_bill = 0
    list_bill = []
    $('#total_bill').val(total_bill)
    pushNotification('Reset new Session', 'Đã reset phiên làm việc mới', 'info')
}


// function to add new bill to Table
function add_new_bill() {
    // get bill code from input text
    var input_bill = $('#bill_input').val().trim();

    check = check_bill_code(input_bill)

    if (!check) {
        return
    }

    // Call API to kiotviet to get information of this bill_code
    $.ajax({
            url: '/shipper/search-bill/',
            type: 'GET',
            data: {
                'bill': input_bill
            },
            success: function(data_response) {
                // Hiển thị kết quả trả về từ máy chủ
                console.log(data_response)
                // var customer_name = data.customer_name
                // var phone = data_response.customer_phone
                // var address = data_response.address
                // var bill = data_response.bill

                // Calculate total_bill money:
                total_bill += data_response.bill

                // Fill data to table
                $("#datatables-basic tbody").append(
                    '<tr id="' + input_bill + '">' +
                    '<td id="' + 'stt_' + input_bill + '">' + ++count + '</td>' +
                    '<td>' + input_bill + '</td>' +
                    '<td>' + data_response.customer_name + '</td>' +
                    '<td>' + data_response.customer_phone + '</td>' +
                    '<td>' + data_response.address + '</td>' +
                    '<td id="' + 'bill_' + input_bill + '">' + new Intl.NumberFormat().format(data_response.bill) + '</td>' +
                    '<td class="table-action width-table-action">' +
                    '<a href="#"  onclick="delete_one_bill(\'' + input_bill + '\')"><i class="fa-regular fa-trash-can"></i></a>' +
                    '</td>' +
                    '</tr>'
                )

                // Update total bill
                $('#total_bill').val(new Intl.NumberFormat().format(total_bill));
                // Clear input bill
                $('#bill_input').val('');
                $('#bill_input').focus();

                pushNotification('Add new bill', 'Thêm bill thành công !', 'success')
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    // This block should code to complete this feature
}


// function to call add new bill by enter key
$('#bill_input').keypress(function (event) {
    // Kiểm tra nếu phím nhấn là Enter (keyCode 13)
    if (event.which == 13) {
        add_new_bill()
    }
})

// function to delete one row
function delete_one_bill(bill_code) {
    // get money of bill and subtract from total money
    var bill_money = $('#bill_' + bill_code).text()
    total_bill -= parseInt(bill_money.replace('.', ''))
    // Update total bill
    $('#total_bill').val(new Intl.NumberFormat().format(total_bill))

    // remove this row
    $('#' + bill_code).remove()

    // Decrease the counter
    count -= 1

    // get index of element which is going to delete
    index = list_bill.indexOf(bill_code)

    // update STT bigger than item deleted to lower
    for (i = index + 1; i < list_bill.length; i++) {
        $('td#stt_' + list_bill[i]).text(i);
        // console.log(i)
    }

    // actually remove it from array
    list_bill.splice(index, 1)

    pushNotification('Delete Bill', 'Xóa bill thành công !', 'success')
}