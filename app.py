from flask import Flask, request, jsonify
from steel_calc import compute_all

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        # 必须的6个参数
        required = ['width_mm', 'height_mm', 'area_single_cm2',
                    'inertia_single_cm4', 'modulus_single_cm3',
                    'inertia_per_meter_cm4']
        missing = [r for r in required if r not in data]
        if missing:
            return jsonify({"error": f"Missing parameters: {missing}"}), 400

        params = {k: float(data[k]) for k in required}
        result = compute_all(params)

        # 将 None 转为 null (JSON 友好)
        for k, v in result.items():
            if v is None:
                result[k] = None

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": f"Invalid number format: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)