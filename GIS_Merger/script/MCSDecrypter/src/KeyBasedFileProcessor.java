
/**
 * Created by bishakh on 2/9/18.
 */


import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.security.NoSuchProviderException;
import java.security.SecureRandom;
import java.security.Security;
import java.util.Iterator;

import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;
import org.bouncycastle.bcpg.ArmoredOutputStream;
import org.bouncycastle.bcpg.CompressionAlgorithmTags;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.openpgp.PGPCompressedData;
import org.bouncycastle.openpgp.PGPEncryptedData;
import org.bouncycastle.openpgp.PGPEncryptedDataGenerator;
import org.bouncycastle.openpgp.PGPEncryptedDataList;
import org.bouncycastle.openpgp.PGPException;
import org.bouncycastle.openpgp.PGPLiteralData;
import org.bouncycastle.openpgp.PGPOnePassSignatureList;
import org.bouncycastle.openpgp.PGPPrivateKey;
import org.bouncycastle.openpgp.PGPPublicKey;
import org.bouncycastle.openpgp.PGPPublicKeyEncryptedData;
import org.bouncycastle.openpgp.PGPSecretKeyRingCollection;
import org.bouncycastle.openpgp.PGPUtil;
import org.bouncycastle.openpgp.jcajce.JcaPGPObjectFactory;
import org.bouncycastle.openpgp.operator.jcajce.JcaKeyFingerprintCalculator;
import org.bouncycastle.openpgp.operator.jcajce.JcePGPDataEncryptorBuilder;
import org.bouncycastle.openpgp.operator.jcajce.JcePublicKeyDataDecryptorFactoryBuilder;
import org.bouncycastle.openpgp.operator.jcajce.JcePublicKeyKeyEncryptionMethodGenerator;
import org.bouncycastle.util.io.Streams;

/**
 * A simple utility class that encrypts/decrypts public key based
 * encryption files.
 * <p>
 * To encrypt a file: KeyBasedFileProcessor -e [-a|-ai] fileName publicKeyFile.<br>
 * If -a is specified the output file will be "ascii-armored".
 * If -i is specified the output file will be have integrity checking added.
 * <p>
 * To decrypt: KeyBasedFileProcessor -d fileName secretKeyFile passPhrase.
 * <p>
 * Note 1: this example will silently overwrite files, nor does it pay any attention to
 * the specification of "_CONSOLE" in the filename. It also expects that a single pass phrase
 * will have been used.
 * <p>
 * Note 2: if an empty file name has been specified in the literal data object contained in the
 * encrypted packet a file with the name filename.out will be generated in the current working directory.
 */
public class KeyBasedFileProcessor
{
    private static void decryptFile(
            String inputFileName,
            String keyPrivFileName,
            String keyPubFileName,
            char[] passwd,
            String defaultFileName,
            String outputFilePath)
            throws IOException, NoSuchProviderException
    {
        InputStream in = new BufferedInputStream(new FileInputStream(inputFileName));
        InputStream keyPrivIn = new BufferedInputStream(new FileInputStream(keyPrivFileName));

        decryptFile(in, inputFileName, keyPrivIn, keyPubFileName, passwd, defaultFileName, outputFilePath);
        keyPrivIn.close();
        in.close();
    }

    /**
     * decrypt the passed in message stream
     */
//    private static void decryptFile(
//            InputStream in,
//            InputStream keyIn,
//            char[]      passwd,
//            String      defaultFileName,
//            String outputFilePath)
//            throws IOException, NoSuchProviderException
//    {
//        in = PGPUtil.getDecoderStream(in);
//
//        try
//        {
//            JcaPGPObjectFactory pgpF = new JcaPGPObjectFactory(in);
//            PGPEncryptedDataList    enc;
//
//            Object                  o = pgpF.nextObject();
//            //
//            // the first object might be a PGP marker packet.
//            //
//            if (o instanceof PGPEncryptedDataList)
//            {
//                enc = (PGPEncryptedDataList)o;
//            }
//            else
//            {
//                enc = (PGPEncryptedDataList)pgpF.nextObject();
//            }
//
//            //
//            // find the secret key
//            //
//            Iterator                    it = enc.getEncryptedDataObjects();
//            PGPPrivateKey               sKey = null;
//            PGPPublicKeyEncryptedData   pbe = null;
//            PGPSecretKeyRingCollection  pgpSec = new PGPSecretKeyRingCollection(
//                    PGPUtil.getDecoderStream(keyIn), new JcaKeyFingerprintCalculator());
//
//            while (sKey == null && it.hasNext())
//            {
//                pbe = (PGPPublicKeyEncryptedData)it.next();
//
//                sKey = PGPExampleUtil.findSecretKey(pgpSec, pbe.getKeyID(), passwd);
//            }
//
//            if (sKey == null)
//            {
//                throw new IllegalArgumentException("secret key for message not found.");
//            }
//
//            InputStream         clear = pbe.getDataStream(new JcePublicKeyDataDecryptorFactoryBuilder().setProvider(new BouncyCastleProvider()).build(sKey));
//
//            JcaPGPObjectFactory    plainFact = new JcaPGPObjectFactory(clear);
//
//            Object              message = plainFact.nextObject();
//
//            if (message instanceof PGPCompressedData)
//            {
//                PGPCompressedData   cData = (PGPCompressedData)message;
//                JcaPGPObjectFactory    pgpFact = new JcaPGPObjectFactory(cData.getDataStream());
//
//                message = pgpFact.nextObject();
//            }
//
//            if (message instanceof PGPLiteralData)
//            {
//                PGPLiteralData ld = (PGPLiteralData)message;
//
//                String outFileName = ld.getFileName();
//                if (outFileName.length() == 0)
//                {
//                    outFileName = defaultFileName;
//                }
//
//                InputStream unc = ld.getInputStream();
//                OutputStream fOut = new BufferedOutputStream(new FileOutputStream(outputFilePath + File.separator +outFileName));
//
//                Streams.pipeAll(unc, fOut);
//
//                fOut.close();
//            }
//            else if (message instanceof PGPOnePassSignatureList)
//            {
//                throw new PGPException("encrypted message contains a signed message - not literal data.");
//            }
//            else
//            {
//                throw new PGPException("message is not a simple encrypted file - type unknown.");
//            }
//
//            if (pbe.isIntegrityProtected())
//            {
//                if (!pbe.verify())
//                {
//                    System.err.println("message failed integrity check");
//                }
//                else
//                {
//                    System.err.println("message integrity check passed");
//                }
//            }
//            else
//            {
//                System.err.println("no message integrity check");
//            }
//        }
//        catch (PGPException e)
//        {
//            System.err.println(e);
//            if (e.getUnderlyingException() != null)
//            {
//                e.getUnderlyingException().printStackTrace();
//            }
//        }
//    }


    /**
     * decrypt the passed in message stream
     */
    private static void decryptFile(
            InputStream in,
            String originalFileNamme,
            InputStream keyPrivIn,
            String keyPubIn,
            char[]      passwd,
            String defaultFileName,
            String outputFilePath)
            throws IOException, NoSuchProviderException
    {
        in= PGPUtil.getDecoderStream(in);
        try
        {
            JcaPGPObjectFactory pgpF = new JcaPGPObjectFactory(in);
            PGPEncryptedDataList    enc;

            Object o = pgpF.nextObject();
            //
            // the first object might be a PGP marker packet.
            //
            if (o instanceof PGPEncryptedDataList)
            {
                enc = (PGPEncryptedDataList)o;
            }
            else
            {
                enc = (PGPEncryptedDataList)pgpF.nextObject();
            }

            //
            // find the secret key
            //
            System.out.println("SIGNED" + " Finding the secret key");
            Iterator it = enc.getEncryptedDataObjects();
            System.out.println("SIGNED" + " After IT");
            PGPPrivateKey               sKey = null;
            PGPPublicKeyEncryptedData   pbe = null;
            PGPSecretKeyRingCollection  pgpSec = new PGPSecretKeyRingCollection(
                    PGPUtil.getDecoderStream(keyPrivIn), new JcaKeyFingerprintCalculator());
            System.out.println("SIGNED" + "After pgpSec");
            while (sKey == null && it.hasNext())
            {
                System.out.println("SIGNED" + "In While");
                pbe = (PGPPublicKeyEncryptedData)it.next();
                sKey = PGPExampleUtil.findSecretKey(pgpSec, pbe.getKeyID(), passwd);
            }

            if (sKey == null)
            {
                System.out.println("SIGNED" + " Key not found");
                throw new IllegalArgumentException("Invalid Argument: secret key for message not found.");
            }
            else{
                System.out.println("SIGNED " + " Secret key found");
            }

            InputStream clear = pbe.getDataStream(new JcePublicKeyDataDecryptorFactoryBuilder().setProvider(new BouncyCastleProvider()).build(sKey));

            JcaPGPObjectFactory    plainFact = new JcaPGPObjectFactory(clear);

            Object message = plainFact.nextObject();

            if (message instanceof PGPCompressedData)
            {
                PGPCompressedData   cData = (PGPCompressedData)message;
                JcaPGPObjectFactory    pgpFact = new JcaPGPObjectFactory(cData.getDataStream());
                message = pgpFact.nextObject();
            }

            if (message instanceof PGPLiteralData)
            {
                PGPLiteralData ld = (PGPLiteralData)message;

                String outFileName = ld.getFileName();
                if (outFileName.length() == 0)
                {
                    outFileName = defaultFileName;
                }

                InputStream unc = ld.getInputStream();

                //Output path
//                File file = Environment.getExternalStoragePublicDirectory("DMS/KML/Dest/SourceKml/"+outFileName);
//                OutputStream fOut = new BufferedOutputStream(new FileOutputStream(file.getAbsolutePath()));
//
//                Streams.pipeAll(unc, fOut);
//                File latestKml = Environment.getExternalStoragePublicDirectory("DMS/KML/Dest/LatestKml/"+FilenameUtils.getBaseName(outFileName)+"_0.kml");
//                FileUtils.copyFile(file,latestKml);
//                fOut.close();
                System.out.println("SIGNED" + " After Decrypt");
                File temp_file = new File(outputFilePath + "/tempDecrypt/" + outFileName);
                OutputStream fOut = new BufferedOutputStream(new FileOutputStream(temp_file.getAbsolutePath()));
                Streams.pipeAll(unc, fOut);
                fOut.close();
                System.out.println("SIGNED" + " Output"+temp_file.getAbsolutePath());
                String source = temp_file.getName().split("_")[1];
                String pubKey;
//                if(file.getName().contains("volunteer")){
//                    System.out.println("SIGNED","Using volunteers pub key");
//                    pubKey = Environment.getExternalStoragePublicDirectory("DMS/Working/pgpKey/pub_volunteer.bgp").getAbsolutePath();
//                }
//                else if(file.getName().contains("user")){
//                    System.out.println("SIGNED","Using users pub key");
//                    pubKey = Environment.getExternalStoragePublicDirectory("DMS/Working/pgpKey/pub_user.bgp").getAbsolutePath();
//                }
//                else {
//                    System.out.println("SIGNED","Using normal pub key");
//                    pubKey = Environment.getExternalStoragePublicDirectory("DMS/Working/pgpKey/pub_" + source + ".bgp").getAbsolutePath();
//                }
                pubKey = keyPubIn;
                if(temp_file.getName().contains("asc")){
                    SignedFileProcessor sfg = new SignedFileProcessor();
                    System.out.println("SIGNED" + " Inside unsigning process");
                    File f = new File(outputFilePath + "/" + FilenameUtils.getBaseName(outFileName)+".kml");
                    if(sfg.verifyFile(temp_file.getAbsolutePath(),pubKey,f.getAbsolutePath())){
                        System.out.println("SIGNED" + " Verified");
                    }
                    else{
                        System.out.println("SIGNED" + " Not Verified");
                    }
//                    File latestKml = new File(outputFilePath +"/" + FilenameUtils.getBaseName(outFileName)+"_0.kml" );
//                    File s = new File()Environment.getExternalStoragePublicDirectory("DMS/KML/Dest/SourceKml/"+FilenameUtils.getBaseName(outFileName)+".kml");
//                    FileUtils.copyFile(s,latestKml);
//                    FileUtils.forceDelete(file);
                }
                else{
                    File s = new File(outputFilePath + "/" + FilenameUtils.getBaseName(outFileName)+".kml");
                    FileUtils.moveFile(temp_file,s);
//                    File latestKml = Environment.getExternalStoragePublicDirectory("DMS/KML/Dest/LatestKml/"+FilenameUtils.getBaseName(outFileName)+"_0.kml");
//                    FileUtils.copyFile(s,latestKml);
                }
            }
            else if (message instanceof PGPOnePassSignatureList)
            {
                System.out.println("SIGNED" + " encrypted message contains a signed message - not literal data.");
                throw new PGPException("encrypted message contains a signed message - not literal data.");
            }
            else
            {
                System.out.println("SIGNED" + " message is not a simple encrypted file - type unknown.");
                throw new PGPException("message is not a simple encrypted file - type unknown.");
            }

            if (pbe.isIntegrityProtected())
            {
                if (!pbe.verify())
                {
                    System.err.println("message failed integrity check");
                }
                else
                {
                    System.err.println("message integrity check passed");
                }
            }
            else
            {
                System.err.println("no message integrity check");
            }
        }
        catch (PGPException e)
        {
            System.err.println(e);
            if (e.getUnderlyingException() != null)
            {
                e.getUnderlyingException().printStackTrace();
            }
        }
    }

    private static void encryptFile(
            String          outputFileName,
            String          inputFileName,
            String          encKeyFileName,
            boolean         armor,
            boolean         withIntegrityCheck)
            throws IOException, NoSuchProviderException, PGPException
    {
        OutputStream out = new BufferedOutputStream(new FileOutputStream(outputFileName));
        PGPPublicKey encKey = PGPExampleUtil.readPublicKey(encKeyFileName);
        encryptFile(out, inputFileName, encKey, armor, withIntegrityCheck);
        out.close();
    }

    private static void encryptFile(
            OutputStream    out,
            String          fileName,
            PGPPublicKey    encKey,
            boolean         armor,
            boolean         withIntegrityCheck)
            throws IOException, NoSuchProviderException
    {
        if (armor)
        {
            out = new ArmoredOutputStream(out);
        }

        try
        {
            byte[] bytes = PGPExampleUtil.compressFile(fileName, CompressionAlgorithmTags.ZIP);

            PGPEncryptedDataGenerator encGen = new PGPEncryptedDataGenerator(
                    new JcePGPDataEncryptorBuilder(PGPEncryptedData.CAST5).setWithIntegrityPacket(withIntegrityCheck).setSecureRandom(new SecureRandom()).setProvider(new BouncyCastleProvider()));

            encGen.addMethod(new JcePublicKeyKeyEncryptionMethodGenerator(encKey).setProvider(new BouncyCastleProvider()));

            OutputStream cOut = encGen.open(out, bytes.length);

            cOut.write(bytes);
            cOut.close();

            if (armor)
            {
                out.close();
            }
        }
        catch (PGPException e)
        {
            System.err.println(e);
            if (e.getUnderlyingException() != null)
            {
                e.getUnderlyingException().printStackTrace();
            }
        }
    }

    public static void main(
            String[] args)
            throws Exception
    {
        Security.addProvider(new BouncyCastleProvider());

        if (args.length == 0)
        {
            System.err.println("usage: KeyBasedFileProcessor -e|-d [-a|ai] file [secretKeyFile passPhrase|pubKeyFile]");
            return;
        }

        if (args[0].equals("-e"))
        {
            if (args[1].equals("-a") || args[1].equals("-ai") || args[1].equals("-ia"))
            {
                encryptFile(args[2] + ".asc", args[2], args[3], true, (args[1].indexOf('i') > 0));
            }
            else if (args[1].equals("-i"))
            {
                encryptFile(args[2] + ".bpg", args[2], args[3], false, true);
            }
            else
            {
                encryptFile(args[1] + ".bpg", args[1], args[2], false, false);
            }
        }
        else if (args[0].equals("-d"))
        {
            //decryptFile(args[1], args[2], args[3].toCharArray(), new File(args[1]).getName() + ".out", "decryptPath");
        }
        else
        {
            System.err.println("usage: KeyBasedFileProcessor -d|-e [-a|ai] file [secretKeyFile passPhrase|pubKeyFile]");
        }
    }

    public static void encrypt(
            String inputFilePath,
            String publicKeyPath
            )
            throws Exception
    {
        Security.addProvider(new BouncyCastleProvider());
        encryptFile(inputFilePath + ".bpg", inputFilePath, publicKeyPath, false, false);
    }

    public static void decrypt(
            String inputFilePath,
            String keyPrivFilePath,
            String keyPubFilePath,
            String passphrase,
            String outputFilePath)
            throws Exception
    {
        Security.addProvider(new BouncyCastleProvider());
        decryptFile(inputFilePath, keyPrivFilePath,keyPubFilePath, passphrase.toCharArray(), new File(inputFilePath) + "out", outputFilePath);
    }
}