<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>株価変動チャート</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-chart-financial/dist/chartjs-chart-financial.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/moment@2.29.4/moment.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-moment@1.0.0"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
      background-color: #222;
      color: white;
    }

    #chart-container {
      width: 90%;
      max-width: 800px;
    }

    canvas {
      width: 100%;
      height: auto;
    }
  </style>
</head>
<body>
  <h1>株価変動チャート</h1>
  <div id="chart-container">
    <canvas id="stockChart"></canvas>
  </div>
  <script>
    // App ScriptのURL (デプロイIDを含むURLに変更)
    const apiUrl = "https://script.google.com/macros/s/AKfycbyiBTNsJVWpbU2qG4UPfuyqfkenSioR9XKNzFRrc305LJd8wNCTLISv-VCwSdnr1ktv/exec?action=getStockPriceByCompany&companyName=APA-KASUMI";

    // データを取得しチャートを描画
    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          const stockData = data.data;

          // Chart.js用のデータ形式に変換
          const chartData = stockData.map((item) => ({
            x: item.date, // 日付
            o: item.open, // 始値
            h: item.high, // 高値
            l: item.low,  // 安値
            c: item.close // 終値
          }));

          // Chart.jsでチャートを描画
          const ctx = document.getElementById("stockChart").getContext("2d");
          new Chart(ctx, {
            type: "candlestick",
            data: {
              datasets: [
                {
                  label: "APA-KASUMI 株価チャート",
                  data: chartData,
                  color: {
                    up: "rgb(75, 192, 192)",   // 上昇時の色
                    down: "rgb(255, 99, 132)", // 下落時の色
                    unchanged: "rgb(200, 200, 200)" // 変化なし
                  }
                }
              ]
            },
            options: {
              responsive: true,
              plugins: {
                legend: {
                  labels: {
                    color: "white" // 凡例の文字色
                  }
                },
                tooltip: {
                  callbacks: {
                    label: (context) => {
                      const data = context.raw;
                      return [
                        `Open: ${data.o}`,
                        `High: ${data.h}`,
                        `Low: ${data.l}`,
                        `Close: ${data.c}`
                      ];
                    }
                  }
                }
              },
              scales: {
                x: {
                  type: "time",
                  time: {
                    unit: "day",
                    tooltipFormat: "YYYY-MM-DD"
                  },
                  grid: {
                    color: "rgba(255, 255, 255, 0.1)"
                  },
                  ticks: {
                    color: "white"
                  }
                },
                y: {
                  grid: {
                    color: "rgba(255, 255, 255, 0.1)"
                  },
                  ticks: {
                    color: "white"
                  }
                }
              }
            }
          });
        } else {
          document.body.innerHTML = `<p>Error: ${data.message}</p>`;
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        document.body.innerHTML = `<p>Error fetching data: ${error.message}</p>`;
      });
  </script>
</body>
</html>
