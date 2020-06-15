// create the game
async function postData(serviceURL) {
    var requestBody = {
        user_score: 0, 
        user_answer:""
    };

    var requestParam = {
        method: 'POST', 
        headers: { "Content-Type": "application/json" }, 
        mode: 'cors',
        body: JSON.stringify(requestBody)
    }

    try {
        const response = await fetch(serviceURL, requestParam);
        if (!response.ok){
            alert('failed');
        } else{
            const data = await response.json();
            // alert('Game successfully started!');
            // reload();
        }
    } catch (error) {
        console.error(error);
    }
}

async function getData(serviceURL) {
    try {
        const response =
            await fetch(serviceURL, { method: 'GET', mode: 'cors' });
        if (!response.ok){
            alert('failed');
        } else{
            const data = await response.json();
            return "http://127.0.0.1:7000/games/"+data;
            alert('Game successfully started!');
        }
    } catch (error) {
        console.error(error);
    }
}

async function displayTable() {
    try {
        tmp = await getData("http://127.0.0.1:7000/games/find_latest");
        const response = await fetch(tmp, { method: 'GET', mode: 'cors' });
        if (!response.ok){
            alert('failed');
        } else{
            const data = await response.json();
            console.log(data);
            var rows = "<div id='board'>";
            var count = 0;
            var eachRow = "";
            eachRow += "<div class='row'>";
            var board = data.board.split(",");
            for (i = 0; i < board.length; i++) {
                if (i%4==0 && i!=0) {
                    eachRow += "</div>";
                    rows += eachRow;
                    eachRow = "<div class='row'>";
                }
                eachRow += 
                        "<div class='boggle'>" +
                            "<span>"+board[i]+"</span>" +
                        "</div>";
        }
        eachRow += "</div>";
        rows += eachRow;
        rows += "</div>";
        console.log(rows)
        $('#board').html(rows);
        }
    } catch (error) {
        console.error(error);
    }
}

var serviceURL = "http://127.0.0.1:7000/games";
postData(serviceURL);
displayTable();

