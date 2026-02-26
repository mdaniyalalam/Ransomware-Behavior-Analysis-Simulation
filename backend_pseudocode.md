# Cryptox Core: System Architecture & Cryptographic Engine

**Authors:** Muhammad Daniyal Alam, Muhammad Rohaan Zaidi, Hassan Arif  
**Purpose:** Educational simulation of ransomware mechanics, hybrid encryption, and inter-process communication.  
**Disclaimer:** This is an architectural overview of an educational sandbox. Dangerous file I/O operations and low-level memory manipulations that were originally 
implemented in C++ have been abstracted for safety and to prevent misuse.

---

## 1️⃣ Global Definitions & Cryptographic Standards

```cpp
// Defined limitations to prevent unintended system impact
CONSTANT ALLOWED_EXTENSIONS = { ".txt", ".docx", ".pdf", ".png", ".jpg" }
CONSTANT RESTRICTED_SYSTEM_PATHS = { "/system/", "/protected_program_files/" }

STRUCTURE RSA_Architecture:
    PrivateKey (2048-bit)
    PublicKey (2048-bit)

STRUCTURE Session_Architecture:
    AES_Symmetric_Key (256-bit)
    AES_Initialization_Vector (128-bit)
    HMAC_Authentication_Key (256-bit)
```
---

## 2️⃣ Environment Initialization & Key Hierarchy

```cpp
CLASS KeyManagementService
  METHOD SetupSimulationEnvironment():
      // Guarantee safety directory is present before any simulation begins
      VERIFY_OR_CREATE_DIRECTORY("/simulation_backup/")
      RETURN GenerateAppDataPath("CryptoxData")
  
  METHOD ManageMasterKeys(configPath):
      IF MasterKeys_Exist_Locally():
          RETURN Load_Keys(configPath)
      ELSE:
          // Simulate the generation of a persistent machine identity
          keys = Generate_RSA2048_KeyPair()
          Save_Keys_Locally(keys, configPath)
          RETURN keys
  
  METHOD SecureSessionKeys(folderPath, PublicKey):
      // Lock the symmetric session keys using the public asymmetric key
      sessionData = Read_Session_Keys(folderPath)
      encryptedSessionData = RSA_OAEP_Encrypt(sessionData, PublicKey)
      Save_Locked_Keys(folderPath, encryptedSessionData)
      Destroy_Plaintext_Keys(folderPath)
  
  METHOD UnlockSessionKeys(folderPath, PrivateKey):
      // Unlock the session keys for the recovery phase
      lockedSessionData = Read_Locked_Keys(folderPath)
      decryptedSessionData = RSA_OAEP_Decrypt(lockedSessionData, PrivateKey)
      Save_Unlocked_Keys(folderPath, decryptedSessionData)
```
---

## 3️⃣ Mandatory Safety Failsafe (Non-Bypassable)

This module ensures that the program behaves strictly as a simulation. It prevents data loss by mandating backups before any cryptographic transformation occurs.

```cpp
CLASS SecurityFailsafe
  METHOD ValidateTarget(file):
      // Ensure critical system files are never touched
      IF file.path IN RESTRICTED_SYSTEM_PATHS:
          RETURN FALSE
      RETURN file.extension IN ALLOWED_EXTENSIONS
  
  METHOD ExecutePreEncryptionBackup(file):
      // Time Complexity: O(S) where S is file size
      // Hardcoded safety net: copies original to an isolated environment
      TRY:
          backupDestination = "/simulation_backup/" + file.name
          Copy_To_Safe_Zone(file.path, backupDestination)
          Log_Event("Failsafe triggered: File secured.")
      CATCH Exception:
          Log_Event("Failsafe failed. Halting process.")
          HALT_EXECUTION()
```
---

## 4️⃣ Abstracted Cryptographic Engine

This section details the theoretical Encrypt-then-MAC workflow without providing actionable file-destruction code.

```cpp
CLASS CryptographicSimulator
  METHOD SimulateEncryptionPhase(file, SessionKeys):
      // 1. Symmetric Encryption (Confidentiality)
      cipherText = Apply_AES256_CBC(file.data, SessionKeys.AES_Key, SessionKeys.AES_IV)
  
      // 2. Message Authentication (Integrity)
      macTag = Calculate_HMAC_SHA256(cipherText, SessionKeys.MAC_Key)
  
      // 3. Assemble and replace (Abstracted for safety)
      assembledDataBlock = macTag + cipherText
      Replace_Original_With_Simulation_Block(file.path, assembledDataBlock)
  
  METHOD SimulateRecoveryPhase(encryptedFile, SessionKeys):
      // 1. Separate components
      storedMacTag = Extract_MAC(encryptedFile)
      cipherText = Extract_Ciphertext(encryptedFile)
  
      // 2. Cryptographic Integrity Verification
      calculatedMacTag = Calculate_HMAC_SHA256(cipherText, SessionKeys.MAC_Key)
      
      IF NOT Secure_Constant_Time_Compare(storedMacTag, calculatedMacTag):
          Log_Event("Integrity Check Failed: File modified post-encryption.")
          Quarantine_File(encryptedFile)
          RETURN ERROR
          
      // 3. Decrypt and restore
      plainText = Apply_AES256_CBC_Decrypt(cipherText, SessionKeys.AES_Key, SessionKeys.AES_IV)
      Restore_Original_File(encryptedFile, plainText)
```
---

## 5️⃣ Simulation Controller

```cpp
CLASS SimulationController
  METHOD RunEncryptionSimulation(targetFolder, MasterKeys):
      SessionKeys = Generate_Random_Session_Architecture()
      actionPerformed = FALSE
  
      FOR EACH file IN Directory_Tree(targetFolder):
          IF SecurityFailsafe.ValidateTarget(file):
              // The backup must succeed before encryption is allowed
              SecurityFailsafe.ExecutePreEncryptionBackup(file)
              CryptographicSimulator.SimulateEncryptionPhase(file, SessionKeys)
              actionPerformed = TRUE
  
      IF actionPerformed:
          KeyManagementService.SecureSessionKeys(targetFolder, MasterKeys.PublicKey)
      
      Secure_Wipe_Memory(SessionKeys)
  
  METHOD RunDecryptionSimulation(targetFolder, MasterKeys):
      KeyManagementService.UnlockSessionKeys(targetFolder, MasterKeys.PrivateKey)
      SessionKeys = Load_Unlocked_Session_Keys(targetFolder)
  
      FOR EACH file IN Directory_Tree(targetFolder):
          IF file.is_encrypted_variant():
              CryptographicSimulator.SimulateRecoveryPhase(file, SessionKeys)
  
      Clean_Up_Session_Artefacts(targetFolder)
      Secure_Wipe_Memory(SessionKeys)
```
---










