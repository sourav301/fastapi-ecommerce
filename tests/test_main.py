def test_add_product(client):
    product_data = {
        "id": 321,
        "name": "Laptop",
        "desc": "High-performance"
         
    }
    
    response = client.post("/products/add", json=product_data)

    print("\nResponse JSON:", response.json())  # Debugging

    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"
    assert response.json()["desc"] == "High-performance" 
    assert response.json()["id"] == 321

    response = client.get("/products/")

    print("\nResponse JSON:", response.json())  # Debugging output

    assert response.status_code == 200
    json_response = response.json()

    # Step 3: Validate the added product is in the response
    assert len(json_response) > 0
    assert json_response[0]["name"] == "Laptop"
    assert json_response[0]["desc"] == "High-performance" 
    assert json_response[0]["id"] == 321

