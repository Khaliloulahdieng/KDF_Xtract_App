import pysftp

import streamlit as st
from paramiko import SSHClient, AutoAddPolicy
import os
from pathlib import Path
import easygui


class Extraction:
    # @st.cache(allow_output_mutation=True, suppress_st_warning=True)
    def Connection_Testeur(TESTEUR):
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(AutoAddPolicy())
 
        client.connect(TESTEUR, username="usnam", password="psswd")

        sftp = client.open_sftp()
        # subprocess.call(sftp)

        print("CONNECTION DONE !")
        # st.write("DEBUG")

        # Grouping Testers by types
        S400 = ["server401",
                "server402",
                "server403",
               ]
        S600 = [
            "server601",
            "server602",
            "server603",
        ]
        S530 = [
            "server501",
            "server502",
            "server503",
        ]
   
        if TESTEUR in S400:
            stdin, stdout, stderr = client.exec_command("ls  /data_folder/")
        elif TESTEUR in S600:
            stdin, stdout, stderr = client.exec_command("ls  /data_folder/")
        else:
            stdin, stdout, stderr = client.exec_command("ls  /data_folder/")

        # lot_file = 'CHOIX'
        lot_file = st.selectbox(
            "LIST OF KDF LOTS:", stdout.read().decode().split(), key=1
        )

        if lot_file != "CHOIX":
            local_folder = Path(
                rf"local_folder"
            )
            data = stdout.read().strip()

            # Downloading with PYSFTP
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None

            conn = pysftp.Connection(
                TESTEUR, username="usrnam", password="passwd", cnopts=cnopts
            )

            # TODO - Done: Centralize kdf extraction on magic server
           
            try:
                magic_server = pysftp.Connection(
                    "magicserver", username="usrnam", password="passwd", cnopts=cnopts
                )
            except:
                pass

            lot_name = "DEFAULT"

            lot_name = st.text_input("Please type your file name: ")

            if lot_name != "DEFAULT":
                if st.button("DOWNLOAD"):
                    if lot_name == "":
                        lot_name = os.path.splitext(lot_file)[0]
                    else:
                        lot_name == lot_name

                    # Downloading the diag file from remote server
                    file_name = f"{TESTEUR}_Diagnostic.log"
                    try:
                        sftp = client.open_sftp()
                        conn = pysftp.Connection(
                            TESTEUR, username="usrnam", password="passwd", cnopts=cnopts
                        )
                       magic_server = pysftp.Connection(
                                  "magicserver", username="usrnam", password="passwd", cnopts=cnopts
                         
                        # process = subprocess.Popen(conn)
                        print("LOT_DATA: ", lot_file)
                        try:
                            if TESTEUR in S400:
                                stdin2, stdout2, stderr2 = client.exec_command(
                                    f"sh script.sh {lot_file} {lot_file}\;"
                                )

                                stdout2.channel.recv_exit_status()
                            elif TESTEUR in S600:
                                stdin2, stdout2, stderr2 = client.exec_command(
                                    f"sh script.sh {lot_file} {lot_file}\;"
                                )
                                stdout2.channel.recv_exit_status()
                            else:
                                # TESTEUR in S530:
                                # TODO: Add parser s530 kdf files to delete <TAG>
                                stdin2, stdout2, stderr2 = client.exec_command(
                                    f"sh script.sh {lot_file} {lot_file}\;"
                                )
                                stdout2.channel.recv_exit_status()

                        except:
                            st.write("ERROR EXECUTING PERL:", stderr2.read().decode())

                        file_txt = os.path.splitext(lot_file)[0]
                        print("FILE TXT= ", file_txt)

                        try:
                            if TESTEUR in S400:
                                file_name = sftp.get(
                                    f"/data_folder/{file_txt}.txt",
                                    rf"\\magic_folder\{file_txt}.txt",
                                )
                                file_name = sftp.get(
                                    f"/data_folder/{file_txt}.txt",
                                    rf"\\magic_folder\{file_txt}.csv",
                                )
                                easygui.msgbox(
                                    "The file is downloaded and is available in KDF_Extraction Folder"
                                )
                            elif TESTEUR in S600:
                                # sftp = client.open_sftp()
                                file_name = sftp.get(
                                    f"/data_folder/{file_txt}.txt",
                                    rf"\\magic_folder\{lot_name}.txt",
                                )
                                file_name = sftp.get(
                                    f"/data_folder/{file_txt}.txt",
                                    rf"\\magic_folder\{lot_name}.csv",
                                )
                                easygui.msgbox(
                                    "The file is downloaded and is available in KDF_Extraction Folder"
                                )
                            else:
                                # TESTEUR == S530:
                                file_name = sftp.get(
                                    f"/data_folder/{file_txt}.txt",
                                    rf"\\magic_folder\{file_txt}.txt",
                                )
                                file_name = sftp.get(
                                    f"/data_folder/{file_txt}.txt",
                                    rf"\\magic_folder\{file_txt}.csv",
                                )
                                easygui.msgbox(
                                    "The file is downloaded and is available in KDF_Extraction Folder"
                                )

                        except:
                            # st.write("Error during downloading- be sure that the csv file is closed in excel", stderr.read().decode())
                            easygui.msgbox(
                                "-Please be sure that the csv file is closed in excel\n"
                                "-The file will not be downloaded\n"
                                "-There is a possible connection issue,\n"
                                "-Or Contact the admin"
                            )

                    except:
                        st.error("La connection n est pas etablie")
                st.write(lot_name)
                # lot_name = "DEFAULT"
                # if lot_name != "DEFAULT":
                if TESTEUR in S400:
                    stdin1, stdout1, stderr1 = client.exec_command(
                        f"head -n 200 /data_folder/{lot_file} \;"
                    )
                    st.code(stdout1.read().decode())
                elif TESTEUR in S600:
                    stdin1, stdout1, stderr1 = client.exec_command(
                        f"head -n 200 /data_folder/{lot_file} \;"
                    )
                    st.code(stdout1.read().decode())
                else:
                    # TESTEUR in S530:
                    stdin1, stdout1, stderr1 = client.exec_command(
                        f"head -n 200 /data_folder/{lot_file} \;"
                    )
                    st.code(stdout1.read().decode())

        sftp.close()
        client.close()

    # @st.cache(allow_output_mutation=True, suppress_st_warning=True)
    def dns_to_tester(TESTEUR):
        switcher = {
            "servers...": "dns"
        }
        return switcher.get(TESTEUR, "nothing")

    # Frame stuff
    # @st.cache(allow_output_mutation=True, suppress_st_warning=True)
    def Interface(self):
        st.subheader("KDFXtract: CHOOSE A TESTER FROM THE LIST")

        TESTEUR = st.selectbox(
            " ",
            (
                "CHOIX",
                "servers...."
            ),
            key=2,
        )
        TOOL = "CHOIX"
        if TESTEUR != "CHOIX":
            TOOL = TESTEUR
            dns = Extraction.dns_to_tester(TOOL)
            Extraction.Connection_Testeur(dns)
