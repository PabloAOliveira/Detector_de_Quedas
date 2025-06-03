import cv2
import time

def test_camera():
    print("Testando câmeras disponíveis...")
    
    for i in range(3):
        print(f"\n=== Testando câmera {i} ===")
        cap = cv2.VideoCapture(i)
        
        if not cap.isOpened():
            print(f"Câmera {i}: Não abriu")
            continue
            
        print(f"Câmera {i}: Abriu com sucesso")
        
        # Aguarda inicialização
        time.sleep(2)
        
        # Tenta capturar alguns frames
        for attempt in range(5):
            ret, frame = cap.read()
            print(f"  Tentativa {attempt+1}: ret={ret}, frame={'válido' if ret and frame is not None and frame.size > 0 else 'inválido'}")
            
            if ret and frame is not None and frame.size > 0:
                print(f"  Frame shape: {frame.shape}")
                
                # Mostra a imagem
                cv2.imshow(f"Teste Câmera {i}", frame)
                print("  Pressione qualquer tecla na janela para continuar...")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                break
            
            time.sleep(0.5)
        
        cap.release()

if __name__ == "__main__":
    test_camera()