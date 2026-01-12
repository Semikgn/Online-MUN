from models import db, Country, EventLog

class GameEngine:
    def execute_action(self, source_id, target_id, action_type):
        """
        Gelen emri işler ve veritabanını günceller.
        """
        # Veritabanından ülkeleri bul
        source = Country.query.get(source_id)
        target = Country.query.get(target_id)
        
        message = ""
        
        # --- SENARYO 1: EKONOMİK AMBARGO ---
        if action_type == "embargo":
            # Formül: Kaynağın gücünün %10'u kadar hasar ver
            damage = int(source.economy * 0.10)
            target.economy -= damage
            message = f"🚨 SON DAKİKA: {source.name}, {target.name} ülkesine ağır ambargo uyguladı! Ekonomi {damage} puan çöktü."

        # --- SENARYO 2: SİBER SALDIRI ---
        elif action_type == "cyber_attack":
            # Sabit hasar
            damage = 15
            target.stability -= damage
            target.military -= 5 # Askeri sistemler de biraz etkilenir
            message = f"⚠️ SİBER SAVAŞ: {source.name} hackerları {target.name} altyapısını çökertti. İstikrar %{damage} düştü."

        # --- SENARYO 3: TİCARET ANLAŞMASI (Pozitif) ---
        elif action_type == "trade_deal":
            gain = 10
            source.economy += gain
            target.economy += gain
            message = f"🤝 ANLAŞMA: {source.name} ve {target.name} serbest ticaret bölgesi kurdu. İki taraf da zenginleşiyor."

        # Negatif değer kontrolü (Puanlar 0'ın altına inmesin)
        if target.economy < 0: target.economy = 0
        if target.stability < 0: target.stability = 0
        if target.military < 0: target.military = 0

        new_log = EventLog(message=message)
        db.session.add(new_log)
        
        # Değişiklikleri kaydet
        db.session.commit()
        
        return message