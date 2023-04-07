import multiprocessing

from selenium.webdriver.remote.webdriver import By
from kameleoo import Kameleo
import os
from selenium import webdriver
import germanNameGenerator as namegen
import time
import requests
from kameleo.local_api_client.models.problem_response_py3 import ProblemResponseException
from conditions import WaitForElementPresence, WaitForElementClicable, CodeFromEmail, RemoveFirstLineFile
from dataClass import Data
from multiprocessing import Process, Pipe, Lock, Barrier
from threading import Thread

def runKameleo(conn2, i, lock):
    kameleo = Kameleo(fullName=Data.genFullName())
    #kameleo = Kameleo(profileName="Ilse-Kirchner")
    kameleo.startProfile()
    kameleo.driver.get("https://api.ipify.org")

    conn2.send("Done")
    while True:
        event = conn2.recv()
        match event:
            case "wieprz":
                wieprz()
            case "ktory":
                println("Odpowiedz: " + str(i), lock)
            case "wylacz":
                kameleo.stopProfile()
                kameleo.stopClient()
def wieprz():
    print("wieprz")

def println(message, lock):
    lock.acquire()
    print(message)
    lock.release()


# def chooseMethod(int):
if __name__ == "__main__":
    c = []
    p = []
    lock = Lock()
    #kamelObj = Kameleo(fullName=Dane.fullName())
    for _ in range(5):
        host_conn, process_conn = Pipe()
        c.append([host_conn, process_conn])
    for i in range(5):
        pr = Process(target=runKameleo, args=(c[i][1], i, lock))
        pr.start()
        p.append(pr)
    for i in c:
        message = i[0].recv()
        println(message, lock)


    while True:
        println("Komu wydać rozkazy?: ", lock)
        i = 0
        for proc in p:
            if proc.is_alive():
                println("Processor " + str(i) + " is running...", lock)
            i += 1
        x = int(input())
        println("Jaki rozkaz?: ", lock)
        y = input()
        c[x][0].send(y)

        for i in c:
            if i[0].poll(0):
                data = i[0].recv()
                println(data, lock)



    # kamelObj = Kameleo(profileName="Ilse-Kirchner")
    # kamelObj.startProfile()
    # driver = kamelObj.driver
    # driver.get('https://filman.cc/premium')

    # for p in process:
    #     p.join()


    # while True:
    #     x = input("1 - Wylacz i zapisz   2 - Wylacz bez zapisu  3 - uruchom jeszcze raz 4 - Usuń profil")
    #     if x == '1':
    #         kamelObj.stopProfile()
    #         kamelObj.saveProfile()
    #         kamelObj.stopClient()
    #         break
    #     elif x == '2':
    #         kamelObj.stopProfile()
    #         kamelObj.stopClient()
    #         break
    #     elif x == '3':
    #         kamelObj.stopProfile()
    #         kamelObj.startProfile()
    #     elif x == '4':
    #         kamelObj.stopProfile()
    #         kamelObj.deleteProfile()
    #         kamelObj.stopClient()
    #         break
