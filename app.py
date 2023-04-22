from flask import Flask, jsonify, request
app = Flask(__name__)

def findOptimalContracts(contracts):
    #Sort the contracts by their start hour in ascending order
    sortedContracts = sorted(contracts, key = lambda x: x['start'])
    
    #Initialize the Dynamic Programming table
    n = len(contracts)
    dp = [{'price':0, 'prev': None} for _ in range(n)]
    
    for i in range(n):
        currentIncome = sortedContracts[i]['price']
        currentDuration = sortedContracts[i]['duration']
        prevIdx = None

        for j in range(i):
            if sortedContracts[j]['start'] + sortedContracts[j]['duration'] <= sortedContracts[i]['start']:
                if dp[j]['price'] > dp[i]['price']:
                    dp[i]['price'] = dp[j]['price']
                    prevIdx = j
        dp[i]['price'] += currentIncome
        dp[i]['prev'] = prevIdx
    
    #Find the contract sequence with maximum profit
    maxIncomeIdx = max(range(n), key=lambda i: dp[i]['price'])
    maxIncome = dp[maxIncomeIdx]['price']
    path = []
    currIdx = maxIncomeIdx
    while currIdx is not None:
        path.append(contracts[currIdx]['name'])
        currIdx = dp[currIdx]['prev']
    path.reverse()
            
        
    return {"income": maxIncome,"path": path}


@app.route('/spaceship/optimize', methods=['POST'])
def optimize():
    contracts = request.json
    result = findOptimalContracts(contracts)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)