pragma solidity >=0.7.0 <0.9.0;


contract StoreSensorData{
    string[] date;
    string[] sensor_val;
    string board_name;
    string plugin_name;
    string plugin_id;
    string board_id;
    
    function putBoardDetails(string memory board_id1, string memory board_name1) public {
        board_name = board_name1;
        board_id = board_id1;
    }

    function putPluginDetails(string memory plugin_id1, string memory plugin_name1) public {
        plugin_name = plugin_name1;
        plugin_id = plugin_id1;
    }

    function putSensorData(string memory date1, string memory sensor_val1) public {
        date.push(date1);
        sensor_val.push(sensor_val1);
    }

    function getData() public view returns (string[] memory, string[]memory, string memory, string memory, string memory, string memory) {
        return (date, sensor_val, board_name, plugin_name, plugin_id, board_id);
    }

    function getIndexData(uint256 index) public view returns(string memory, string memory) {
        return (date[index], sensor_val[index]);
    }

    function getTotaLength() public view returns(uint256) {
        return date.length;
    }
}